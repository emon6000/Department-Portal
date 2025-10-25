# notices/admin.py

from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'batch', 'is_for_teachers', 'updated_at')
    list_filter = ('is_for_teachers', 'batch')