# classroom/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Classroom, Booking
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from django.db.models import Prefetch  # <-- ADD THIS IMPORT

def classroom_list_view(request):
    now = timezone.now()
    
    # --- LOGIC FOR CURRENT STATUS ---
    current_bookings = Booking.objects.filter(start_time__lte=now, end_time__gte=now)
    booked_room_ids = current_bookings.values_list('classroom_id', flat=True)

    # --- NEW LOGIC FOR TODAY'S SCHEDULE ---
    
    # 1. Define "end of today"
    end_of_day = now.replace(hour=23, minute=59, second=59)
    
    # 2. Create a query for all bookings from now until the end of the day
    todays_bookings_query = Booking.objects.filter(
        start_time__lte=end_of_day, # Starts today
        end_time__gte=now           # Hasn't ended yet
    ).order_by('start_time')        # Show them in order
    
    # 3. Get all rooms, and "prefetch" their related bookings for today
    #    This is the "best way" to avoid N+1 queries.
    #    It gets all rooms and all bookings in just 2 database queries.
    all_rooms = Classroom.objects.prefetch_related(
        Prefetch(
            'booking_set',
            queryset=todays_bookings_query,
            to_attr='todays_bookings' # Puts the results in 'room.todays_bookings'
        )
    )
    
    # 4. Set the *current* status for each room
    for room in all_rooms:
        if room.id in booked_room_ids:
            room.status = 'In Use'
        else:
            room.status = 'Vacant'
            
    context = {
        'rooms': all_rooms
    }
    return render(request, 'classroom_list.html', context)


@login_required
def create_booking_view(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Only teachers can book classrooms.')
        return redirect('classroom-list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.teacher = request.user
            booking.save()
            
            messages.success(request, f'You have successfully booked {booking.classroom.room_name}!')
            return redirect('classroom-list')
        else:
            # Errors (like conflicts) will be handled by the form
            pass 
    else:
        form = BookingForm()
        
    context = {
        'form': form
    }
    return render(request, 'create_booking.html', context)

# (Add this new view function, maybe after create_booking_view)

@login_required
def my_bookings_view(request):
    # Security check: Only teachers can see this page
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Only teachers have bookings.')
        return redirect('dashboard') # Send them to their dashboard
    
    # Get all bookings made by this specific teacher
    # Order them so the newest bookings appear first
    bookings = Booking.objects.filter(teacher=request.user).order_by('-start_time')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'my_bookings.html', context)

# classroom/views.py
# (Add this new view function)

@login_required
def update_booking_view(request, booking_id):
    # Get the booking, or show a 404 page if it doesn't exist
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: Is this user the owner of this booking?
    if request.user != booking.teacher:
        messages.error(request, 'You do not have permission to edit this booking.')
        return redirect('my-bookings')
    
    if request.method == 'POST':
        # Pass 'instance=booking' to fill the form with the booking's data
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('my-bookings')
    else:
        # Show the form pre-filled with the existing booking data
        form = BookingForm(instance=booking)
        
    context = {
        'form': form
    }
    # We can reuse the create_booking template, but let's make a new one
    # to be clear.
    return render(request, 'update_booking.html', context)

# classroom/views.py
# (Add this new view function)

@login_required
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: User must be the owner
    if request.user != booking.teacher:
        messages.error(request, 'You do not have permission to delete this booking.')
        return redirect('my-bookings')
    
    # If the user clicks the "Confirm" button (which is a POST)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
        return redirect('my-bookings')
    
    # If it's a GET request, just show the confirmation page
    context = {
        'booking': booking
    }
    return render(request, 'delete_booking.html', context)