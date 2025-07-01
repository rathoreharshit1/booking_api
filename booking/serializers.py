from rest_framework import serializers
from .models import Availability, Booking
from datetime import datetime

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')
        date = data.get('date')

        if start is None or end is None or date is None:
            raise serializers.ValidationError("Date, start_time, and end_time are required.")

        if start >= end:
            raise serializers.ValidationError("Start time must be before end time.")

        # Duration check
        duration = datetime.combine(date, end) - datetime.combine(date, start)
        if duration.total_seconds() not in [900, 1800, 2700, 3600]:
            raise serializers.ValidationError("Invalid booking duration. Only 15m, 30m, 45m, or 1hr allowed.")

        return data
