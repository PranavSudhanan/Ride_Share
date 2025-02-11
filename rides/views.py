from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import RideSerializer
from .models import Ride
from rest_framework.decorators import action

class RideViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    
    serializer_class = RideSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_driver == False:
            return Ride.objects.filter(rider=user)
        elif user.is_driver == True:
            return Ride.objects.filter(driver=user)
        return Ride.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

class RideStatusUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        status = request.data.get('status')
        
        if status not in dict(Ride.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        ride.status = status
        ride.save()
        return Response(RideSerializer(ride).data)

class RideTrackingViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    
    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        ride = self.get_object()
        
        # Validate coordinates
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        
        if not (-90 <= float(lat) <= 90) or not (-180 <= float(lon) <= 180):
            return Response({'error': 'Invalid coordinates'},
                          status=status.HTTP_400_BAD_REQUEST)
        
        ride.current_location_lat = lat
        ride.current_location_lon = lon
        ride.save()
        
        return Response(RideSerializer(ride).data)