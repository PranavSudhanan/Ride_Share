from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from users.models import User
from .models import Ride

class RideMatchingService:
    @staticmethod
    def find_available_drivers(ride):
        # Get drivers within reasonable distance
        radius = 5000  # meters
        
        pickup_point = Point(ride.pickup_location_lon, ride.pickup_location_lat)
        
        available_drivers = User.objects.filter(
            user_type='driver',
            status='available'
        ).annotate(
            distance=Distance('location', pickup_point)
        ).filter(distance__lte=radius)
        
        return available_drivers.order_by('distance')[:5]