from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'language', 'stars', 'created_at']
        read_only_fields = ('id', 'created_at')
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Project name cannot be empty")
        return value.strip()
    
    def validate_stars(self, value):
        if value < 0:
            raise serializers.ValidationError("Stars count cannot be negative")
        return value