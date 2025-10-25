# classroom/forms.py

from django import forms
from .models import Booking
from django.utils import timezone  # <-- ADD THIS
from django.db.models import Q     # <-- ADD THIS

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['classroom', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    # --- ADD THIS ENTIRE METHOD ---
    def clean(self):
        # 1. Get the data from the form
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        classroom = cleaned_data.get('classroom')

        # 2. Check that all fields are present (to avoid errors)
        if not start_time or not end_time or not classroom:
            return cleaned_data

        # 3. Check for valid times (end must be after start)
        if end_time <= start_time:
            raise forms.ValidationError("Booking end time must be after the start time.")

        # 4. Check for bookings in the past
        if start_time <= timezone.now():
            raise forms.ValidationError("Cannot book a time in the past.")

        # 5. Check for conflicts (The Overlap Logic)
        # An overlap exists if:
        # (Existing Start < New End) AND (Existing End > New Start)
        
        conflicts = Booking.objects.filter(
            classroom=classroom,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists() # .exists() is faster than .count()

        if conflicts:
            raise forms.ValidationError(
                "This room is already booked for the selected time slot. Please check the schedule."
            )

        # Always return the cleaned data
        return cleaned_data