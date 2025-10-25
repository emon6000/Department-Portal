# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

# Model for Batches
class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "BSc 10th"

    def __str__(self):
        return self.name

# Model to extend the built-in User model
class UserProfile(models.Model):
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    is_cr = models.BooleanField(default=False)

    # --- NEW FIELDS WE ARE ADDING ---
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    # This will create a 'profile_pics' folder inside your media folder
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # --------------------------------

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"