# notices/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice
from .forms import NoticeForm

# notices/views.py

# ... (other imports)

@login_required
def update_teacher_notice_view(request):
    # Security check: Must be a teacher OR an admin
    if not (request.user.is_superuser or (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher')):
        # --- THIS BLOCK MUST BE INDENTED ---
        messages.error(request, 'You do not have permission to edit this notice.')
        return redirect('dashboard')
        # -------------------------------------

    # Get the single teacher notice. If it doesn't exist, create it.
    notice, created = Notice.objects.get_or_create(is_for_teachers=True)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher notice updated!')
            return redirect('dashboard')
    else:
        form = NoticeForm(instance=notice)

    context = {'form': form}
    return render(request, 'update_notice.html', context)

# ... (rest of the file)


@login_required
def update_batch_notice_view(request):
    # Security check: Must be a CR
    if not request.user.userprofile.is_cr:
        messages.error(request, 'Only Class Representatives can edit this notice.')
        return redirect('dashboard')

    # Get the notice for this CR's specific batch
    batch = request.user.userprofile.batch
    notice, created = Notice.objects.get_or_create(batch=batch, is_for_teachers=False)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Batch notice updated!')
            return redirect('dashboard')
    else:
        form = NoticeForm(instance=notice)

    context = {'form': form}
    return render(request, 'update_notice.html', context)