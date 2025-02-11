from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import RideSerializer
from .models import Ride
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):
    """Custom permission to allow only drivers to update ride status and location."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver


class RideViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    Viewset that provides create, list and retrieve actions for Rides.
    """
    
    serializer_class = RideSerializer
    
    def get_queryset(self):
        """Ensure only authorized users can see rides."""
        if self.request.user.is_authenticated and self.request.user.is_driver:
            return Ride.objects.filter(driver=self.request.user)
        elif self.request.user.is_authenticated:
            return Ride.objects.filter(rider=self.request.user)
        return Ride.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a new ride with the requesting user as the rider.
        """
        serializer.save(rider=self.request.user)


class RideStatusUpdateViewSet(viewsets.ModelViewSet):
    """
    Viewset that provides partial update action for updating ride status.

    Only drivers can update ride status.
    """
    queryset = Ride.objects.all()
    permission_classes = [IsDriver]

    def partial_update(self, request, *args, **kwargs):
        """Update ride status only if the request is valid."""
        ride = self.get_object()
        if 'status' in request.data:
            ride.status = request.data['status']
            ride.save()
            return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class RideTrackingViewSet(viewsets.ModelViewSet):
    """
    Viewset that provides partial update action for updating ride current location.

    Only drivers can update ride current location.
    """
    queryset = Ride.objects.all()
    permission_classes = [IsDriver]

    def partial_update(self, request, *args, **kwargs):
        """
        Update ride current location only if the request is valid.

        The request must include 'latitude' and 'longitude' in the request data.
        """
        ride = self.get_object()
        if 'latitude' in request.data and 'longitude' in request.data:
            ride.current_location_lat = request.data['latitude']
            ride.current_location_lon = request.data['longitude']
            ride.save()
            return Response({'message': 'Location updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid location'}, status=status.HTTP_400_BAD_REQUEST)


