import os
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Project

# GitHub API conf
GITHUB_API_BASE = "https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetch_github_repo(request, owner, repo):
    api_url = f"{GITHUB_API_BASE}/{owner}/{repo}"
    
    try:
        response = requests.get(api_url, headers=get_github_headers(), timeout=10)
        
        if response.status_code == 404:
            return Response(
                {"error": f"Repository '{owner}/{repo}' not found. It may be private, deleted, or doesn't exist."},
                status=404
            )
        elif response.status_code == 403:
            return Response(
                {"error": f"Access denied to '{owner}/{repo}'. This repository may be private or you've hit the rate limit."},
                status=403
            )
        elif response.status_code != 200:
            return Response(
                {"error": f"GitHub API returned status {response.status_code}"},
                status=400
            )
        
        repo_data = response.json()
        return Response({
            "name": repo_data.get("name"),
            "description": repo_data.get("description", ""),
            "language": repo_data.get("language"),
            "stars": repo_data.get("stargazers_count", 0),
        })
        
    except requests.RequestException as e:
        return Response(
            {"error": "Failed to connect to GitHub API"},
            status=500
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def save_github_repo(request, owner, repo):
    api_url = f"{GITHUB_API_BASE}/{owner}/{repo}"
    
    try:
        response = requests.get(api_url, headers=get_github_headers(), timeout=10)
        
        if response.status_code == 404:
            return Response(
                {"error": f"Repository '{owner}/{repo}' not found. It may be private, deleted, or doesn't exist."},
                status=404
            )
        elif response.status_code == 403:
            return Response(
                {"error": f"Access denied to '{owner}/{repo}'. This repository may be private or you've hit the rate limit."},
                status=403
            )
        elif response.status_code != 200:
            return Response(
                {"error": f"GitHub API returned status {response.status_code}"},
                status=400
            )
        
        repo_data = response.json()
        
        project, is_new = Project.objects.update_or_create(
            name=repo_data['name'],
            defaults={
                'description': repo_data.get('description', ''),
                'language': repo_data.get('language', ''),
                'stars': repo_data.get('stargazers_count', 0),
            }
        )
        
        action = "imported" if is_new else "updated"
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
        })
        
    except requests.RequestException:
        return Response(
            {"error": "Failed to connect to GitHub API"},
            status=500
        )
    except Exception as e:
        return Response(
            {"error": "An error occurred while saving the repository"},
            status=500
        )

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project_name = project.name
        project.delete()
        
        return Response({
            "message": f"Project '{project_name}' deleted successfully"
        })
        
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found"},
            status=404
        )
    except Exception:
        return Response(
            {"error": "An error occurred while deleting the project"},
            status=500
        )