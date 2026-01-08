from django.db import models

# Create your models here.

class Todo(models.Model):
    text = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.text