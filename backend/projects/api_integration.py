import os
import logging
import requests
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Project

logger = logging.getLogger(__name__)

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REQUEST_TIMEOUT = 10

def get_github_headers():
    """Get headers for GitHub API requests"""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-Repo-Tracker/1.0"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetch_github_repo(request, owner, repo):
    """Fetch repository data from GitHub API without saving"""
    if not owner or not repo:
        return Response(
            {"error": "Owner and repository name are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    api_url = f"{GITHUB_API_BASE}/{owner}/{repo}"
    
    try:
        response = requests.get(
            api_url, 
            headers=get_github_headers(), 
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 404:
            return Response(
                {"error": f"Repository '{owner}/{repo}' not found on GitHub"},
                status=status.HTTP_404_NOT_FOUND
            )
        elif response.status_code == 403:
            return Response(
                {"error": "GitHub API rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        elif response.status_code != 200:
            logger.error(f"GitHub API error: {response.status_code} for {owner}/{repo}")
            return Response(
                {"error": f"GitHub API returned status {response.status_code}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        repo_data = response.json()
        return Response({
            "name": repo_data.get("name"),
            "description": repo_data.get("description", ""),
            "language": repo_data.get("language"),
            "stars": repo_data.get("stargazers_count", 0),
        })
        
    except requests.Timeout:
        logger.error(f"Timeout fetching {owner}/{repo}")
        return Response(
            {"error": "Request timeout - GitHub API is not responding"},
            status=status.HTTP_408_REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error(f"Request error fetching {owner}/{repo}: {str(e)}")
        return Response(
            {"error": "Failed to connect to GitHub API"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def save_github_repo(request, owner, repo):
    """Fetch and save repository data from GitHub API"""
    if not owner or not repo:
        return Response(
            {"error": "Owner and repository name are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    api_url = f"{GITHUB_API_BASE}/{owner}/{repo}"
    
    try:
        response = requests.get(
            api_url, 
            headers=get_github_headers(), 
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 404:
            return Response(
                {"error": f"Repository '{owner}/{repo}' not found on GitHub"},
                status=status.HTTP_404_NOT_FOUND
            )
        elif response.status_code == 403:
            return Response(
                {"error": "GitHub API rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        elif response.status_code != 200:
            logger.error(f"GitHub API error: {response.status_code} for {owner}/{repo}")
            return Response(
                {"error": f"GitHub API returned status {response.status_code}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        repo_data = response.json()
        
        # Validate required fields
        if not repo_data.get('name'):
            return Response(
                {"error": "Invalid repository data received from GitHub"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        project, is_new = Project.objects.update_or_create(
            name=repo_data['name'],
            defaults={
                'description': repo_data.get('description', ''),
                'language': repo_data.get('language', ''),
                'stars': repo_data.get('stargazers_count', 0),
            }
        )
        
        action = "imported" if is_new else "updated"
        logger.info(f"Repository '{project.name}' {action} successfully")
        
        return Response({
            "message": f"Repository '{project.name}' {action} successfully",
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "language": project.language,
                "stars": project.stars,
                "created_at": project.created_at
            }
        }, status=status.HTTP_201_CREATED if is_new else status.HTTP_200_OK)
        
    except requests.Timeout:
        logger.error(f"Timeout saving {owner}/{repo}")
        return Response(
            {"error": "Request timeout - GitHub API is not responding"},
            status=status.HTTP_408_REQUEST_TIMEOUT
        )
    except requests.RequestException as e:
        logger.error(f"Request error saving {owner}/{repo}: {str(e)}")
        return Response(
            {"error": "Failed to connect to GitHub API"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except ValidationError as e:
        logger.error(f"Validation error saving {owner}/{repo}: {str(e)}")
        return Response(
            {"error": "Invalid data provided"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Unexpected error saving {owner}/{repo}: {str(e)}")
        return Response(
            {"error": "An unexpected error occurred while saving the repository"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_project(request, project_id):
    """Delete a project by ID"""
    try:
        project = Project.objects.get(id=project_id)
        project_name = project.name
        project.delete()
        
        logger.info(f"Project '{project_name}' deleted successfully")
        return Response({
            "message": f"Project '{project_name}' deleted successfully"
        }, status=status.HTTP_200_OK)
        
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {str(e)}")
        return Response(
            {"error": "An error occurred while deleting the project"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )