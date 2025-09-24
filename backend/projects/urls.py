from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from .api_integration import fetch_github_repo, save_github_repo

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('projects/', include(router.urls)),
    path('github/<str:owner>/<str:repo>/', fetch_github_repo, name='github-repo'),
    path('github/save/<str:owner>/<str:repo>/', save_github_repo, name='save-github-repo')
]


