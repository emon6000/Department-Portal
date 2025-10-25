# classroom/admin.py

from django.contrib import admin
from .models import Classroom, Booking

# We'll customize the Booking display to be more useful
class BookingAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'teacher', 'start_time', 'end_time')
    list_filter = ('classroom', 'teacher')

admin.site.register(Classroom)
admin.site.register(Booking, BookingAdmin)