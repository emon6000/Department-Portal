# notices/forms.py

from django import forms
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }