# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public URLs
    path('', views.homepage_view, name='homepage'),
    path('teachers/', views.teacher_list_view, name='teacher-list'),
    path('students/', views.batch_list_view, name='batch-list'),
    path('students/<int:batch_id>/', views.student_list_view, name='student-list'),

    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    
    # Dashboard URL
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # --- ADD THIS NEW URL ---
    path('profile/', views.profile_update_view, name='profile-update'),
    # -------------------------
]