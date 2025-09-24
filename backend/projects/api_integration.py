import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project

GITHUB_API_URL = "https://api.github.com/repos"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@api_view(['GET'])
def fetch_github_repo(request, owner, repo):

    url = f"{GITHUB_API_URL}/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return Response({"error": "Could not fetch repo from GitHub"},
                        status=response.status_code)

    data = response.json()
    return Response({
        "name": data.get("name"),
        "description": data.get("description"),
        "language": data.get("language"),
        "stars": data.get("stargazers_count", 0),
    })

@api_view(['POST'])
def save_github_repo(request, owner, repo):
    url = f"{GITHUB_API_URL}/{owner}/{repo}"
    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return Response({"error": f"Could not fetch repo from GitHub"},
                        status=response.status_code)
    
    data = response.json()

    project, created = Project.objects.update_or_create(
        name=data['name'],
        defaults={
            'description': data.get('description', ''),
            'language': data.get('language', ''),
            'stars': data.get('stargazers_count', 0),
        }
    )
    
    return Response({
        "message": "Repo Saved Sucessfully" if created else "Repo updated sucessfully",
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "language": project.language,
            "stars": project.stars,
            "created_at": project.created_at
        }
    })

