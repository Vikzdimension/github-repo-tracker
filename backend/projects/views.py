from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Project
from .serializers import ProjectSerializer

def home_view(request):
    """Render the home page"""
    return render(request, 'home.html')

@staff_member_required
def dashboard_view(request):
    return render(request, 'admin/dashboard.html')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        language = self.request.query_params.get('language')
        
        if language:
            queryset = queryset.filter(language__icontains=language)
            
        return queryset
