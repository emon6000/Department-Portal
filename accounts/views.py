# accounts/views.py

from django.shortcuts import render, redirect  # <-- ADD 'redirect'
from django.contrib.auth.models import User 
from .models import Batch
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm  # <-- ADD THIS IMPORT
from django.contrib import messages          # <-- ADD THIS IMPORT
from notices.models import Notice

# --- Public Views ---
def homepage_view(request):
    return render(request, 'index.html')

def teacher_list_view(request):
    teachers = User.objects.filter(userprofile__role='teacher')
    context = {
        'teachers': teachers
    }
    return render(request, 'teacher_list.html', context)

def batch_list_view(request):
    batches = Batch.objects.all()
    context = {
        'batches': batches
    }
    return render(request, 'batch_list.html', context)

def student_list_view(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    students = User.objects.filter(
        userprofile__role='student',
        userprofile__batch=batch
    )
    context = {
        'students': students,
        'batch': batch,
    }
    return render(request, 'student_list.html', context)

# --- Private (Logged-In) Views ---

@login_required
def dashboard_view(request):
    # Set default values
    notice = None
    user_role = None
    is_cr = False

    # --- THIS IS THE FIX ---

    # 1. Check if the user is an admin (superuser)
    if request.user.is_superuser:
        user_role = 'admin'
        # Let's show the teacher notice board to the admin
        notice = Notice.objects.filter(is_for_teachers=True).first()

    # 2. Check if the user has a profile (for Students and Teachers)
    #    'hasattr' is a safe way to check without crashing
    elif hasattr(request.user, 'userprofile'):
        user_role = request.user.userprofile.role
        is_cr = request.user.userprofile.is_cr

        if user_role == 'teacher':
            notice = Notice.objects.filter(is_for_teachers=True).first()
        elif user_role == 'student':
            batch = request.user.userprofile.batch
            if batch:
                notice = Notice.objects.filter(batch=batch, is_for_teachers=False).first()

    # 3. (Else) The user is logged in but has no role or profile
    #    We'll just show them a basic dashboard.

    context = {
        'notice': notice,
        'user_role': user_role, # This is now 'admin', 'teacher', 'student', or None
        'is_cr': is_cr
    }
    return render(request, 'dashboard.html', context)

# ... (profile_update_view)
# --- ADD THIS NEW VIEW ---
@login_required
def profile_update_view(request):
    # This view handles both GET (showing the form) and POST (submitting data)
    if request.method == 'POST':
        # Create form instances populated with the data from the request
        # We pass 'request.user' to 'instance' to tell the form which user we are editing
        user_form = UserForm(request.POST, instance=request.user)
        
        # We also pass 'request.FILES' to handle the photo upload
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Send a success message to the user
            messages.success(request, 'Your profile has been updated successfully!')
            
            # Redirect back to the dashboard
            return redirect('dashboard')
        else:
            # If forms are invalid, send an error message
            messages.error(request, 'Please correct the errors below.')

    else:
        # This is a GET request, so just show the forms with the user's current data
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile_update.html', context)
# -------------------------