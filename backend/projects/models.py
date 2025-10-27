from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    stars = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'language']),
        ]

    def __str__(self):
        return self.name