# notices/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.update_teacher_notice_view, name='update-teacher-notice'),
    path('batch/', views.update_batch_notice_view, name='update-batch-notice'),
]