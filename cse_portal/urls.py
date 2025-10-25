# cse_portal/urls.py

from django.contrib import admin
from django.urls import path, include  # 'include' should be here
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # --- ADD THIS NEW LINE ---
    path('notices/', include('notices.urls')),

    # --- ADD THIS NEW LINE ---
    # Any URL starting with 'classrooms/' will be handled by our classroom app
    path('classrooms/', include('classroom.urls')),
    # -------------------------

    path('', include('accounts.urls')), # This handles all our other pages
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)