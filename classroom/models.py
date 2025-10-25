# classroom/models.py

from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    room_name = models.CharField(max_length=100) # e.g., "Room 201"
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.room_name

class Booking(models.Model):
    # Link to the teacher who made the booking
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    # Link to the room being booked
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    # Booking time slots
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        # e.g., "Room 201 booked by teacher1 (Oct 25, 2025)"
        return f"{self.classroom.room_name} booked by {self.teacher.username} ({self.start_time.strftime('%b %d, %Y')})"