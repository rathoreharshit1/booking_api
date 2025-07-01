from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
