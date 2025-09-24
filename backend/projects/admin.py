from django.contrib import admin
from django.conf import settings
from .models import Project
import os
import glob

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
        
        # Find asset files dynamically
        static_root = settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'staticfiles')
        assets_path = os.path.join(static_root, 'assets')
        
        css_files = []
        js_files = []
        
        if os.path.exists(assets_path):
            css_files = [f'assets/{os.path.basename(f)}' for f in glob.glob(os.path.join(assets_path, 'index-*.css'))]
            js_files = [f'assets/{os.path.basename(f)}' for f in glob.glob(os.path.join(assets_path, 'index-*.js'))]
        
        extra_context['css_files'] = css_files
        extra_context['js_files'] = js_files
        
        return super().changelist_view(request, extra_context)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


