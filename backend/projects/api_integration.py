import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

GITHUB_API_URL = "https://api.github.com/repos"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@api_view(['GET'])
def fetch_github_trending(request, owner, repo):
    url = f"{GITHUB_API_URL}/{owner}/{repo}"
    headers = {
        "Accept" : "application/vnd.github+json",
        "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({"error": f"Could not fetch repo"}, 
                        status=response.status_code)