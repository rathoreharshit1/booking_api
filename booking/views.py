from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Availability, Booking
from .serializers import AvailabilitySerializer, BookingSerializer
from datetime import datetime

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = data.get('user')
        date = data.get('date')
        start = data.get('start_time')
        end = data.get('end_time')
        weekday = date.weekday()

        # Check availability
        availabilities = Availability.objects.filter(user=user, weekday=weekday)
        within_avail = any(a.start_time <= start and a.end_time >= end for a in availabilities)
        if not within_avail:
            return Response({'error': 'Requested time is not within availability.'}, status=400)

        # Check overlaps
        overlaps = Booking.objects.filter(
            user=user, date=date,
            start_time__lt=end,
            end_time__gt=start
        ).exists()
        if overlaps:
            return Response({'error': 'This time slot is already booked.'}, status=409)

        self.perform_create(serializer)
        return Response({'message': 'Booking created successfully', 'data': serializer.data}, status=201)

    def list(self, request, *args, **kwargs):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response({'message': 'Bookings fetched successfully', 'data': serializer.data}, status=200)

    def retrieve(self, request, *args, **kwargs):
        try:
            booking = self.get_object()
            serializer = self.get_serializer(booking)
            return Response({'message': 'Booking fetched successfully', 'data': serializer.data}, status=200)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

    def partial_update(self, request, *args, **kwargs):
        booking = self.get_object()
        serializer = self.get_serializer(booking, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'message': 'Booking updated successfully', 'data': serializer.data}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            booking = self.get_object()
            self.perform_destroy(booking)
            return Response({'message': 'Booking deleted successfully'}, status=204)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)