from django.apps import AppConfig
from django.db.utils import OperationalError

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    
    def ready(self):
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
        except (OperationalError, Exception):
            pass
