import os
import requests
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect, render
from .models import Project

# Register your models here.
GITHUB_API_URL = "https://api.github.com/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'language', 'stars', 'created_at')
    search_fields = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("fetch-github-repo/", self.admin_site.admin_view(self.fetch_github_repo),
                name="fetch-github-repo"),
        ]
        return custom_urls + urls
    
    def fetch_github_repo(self, request):
        if request.method == "POST":
            owner = request.POST.get("owner")
            repo = request.POST.get("repo")

            if not owner or not repo:
                messages.error(request, "Please provide both owner and repo.")
                return redirect("admin:fetch-github-repo")
            
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
            }

            url = f"{GITHUB_API_URL}/{owner}/{repo}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                project, created = Project.objects.update_or_create(
                    name=f"{owner}/{repo}",
                    defaults={
                        'description': data.get('description', ''),
                        'language': data.get('language', ''),
                        'stars': data.get('stargazers_count', 0),
                    },
                )
                
                msg = "Repo saved sucessfully." if created else "Repo updated sucessfully."
                messages.success(request, msg)
                return redirect("admin:projects_project_changelist")
            else:
                messages.error(request, f"Github API error: {response.status_code}")
                return redirect("admin:fetch-github-repo")
            
        return render(request, "admin/fetch_github_repo.html")
