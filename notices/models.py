# notices/models.py

from django.db import models
from accounts.models import Batch # Import the Batch model from our accounts app

class Notice(models.Model):
    # The content of the notice
    content = models.TextField()

    # This will link to a specific batch (e.g., "BSc 10th")
    # It's allowed to be empty for the teachers' notice
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)

    # This checkbox will be TRUE for the single teacher notice
    is_for_teachers = models.BooleanField(default=False)

    # This will automatically update when the notice is edited
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_for_teachers:
            return "Teacher Notice"
        elif self.batch:
            return f"Notice for {self.batch.name}"
        return "General Notice" # Fallback