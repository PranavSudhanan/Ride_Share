from rest_framework import serializers
from rides.models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        
    def validate_status(self, value):
        valid_statuses = dict(Ride.STATUS_CHOICES)
        if value not in valid_statuses:
            raise serializers.ValidationError('Invalid ride status')
        return value