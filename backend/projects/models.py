from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.TextField(max_length=255)
    description =models.TextField(max_length=255)
    language = models.CharField(max_length=50)
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name