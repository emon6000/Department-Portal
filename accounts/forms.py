# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# This is a 'ModelForm', it automatically builds a form from our User model
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # These are the only fields we want the user to edit
        fields = ['first_name', 'last_name', 'email']

# This is another ModelForm for our UserProfile model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # These are the custom fields we want the user to edit
        fields = ['bio', 'phone', 'profile_photo']