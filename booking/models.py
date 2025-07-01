from django.db import models
from django.contrib.auth.models import User

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=[(i, day) for i, day in enumerate(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )])
    start_time = models.TimeField()
    end_time = models.TimeField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
