from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):    
    list_display = ('name', 'description', 'language', 'stars', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-stars', '-created_at')
    
    change_list_template = 'admin/projects/project/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'GitHub Repository Dashboard'
        return super().changelist_view(request, extra_context)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


