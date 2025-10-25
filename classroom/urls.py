# classroom/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.classroom_list_view, name='classroom-list'),

    # --- ADD THIS NEW URL ---
    path('book/', views.create_booking_view, name='create-booking'),
    # ------------------------
    path('my-bookings/', views.my_bookings_view, name='my-bookings'),
    # The <int:booking_id> part captures the ID from the URL
    path('update/<int:booking_id>/', views.update_booking_view, name='update-booking'),
    # --- ADD THIS NEW URL ---
    path('delete/<int:booking_id>/', views.delete_booking_view, name='delete-booking'),
]