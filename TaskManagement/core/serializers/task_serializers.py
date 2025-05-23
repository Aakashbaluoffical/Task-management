from rest_framework import serializers
from core.models.task_models import Task




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'assigned_to', 'worked_hours', 'completion_report', 'is_active', 'created_at', 'updated_at']  

    def validate(self, attrs):
        if 'title' in attrs and not attrs['title']:
            raise serializers.ValidationError({"error": "Title is empty"})
            
        if attrs.get('title') and Task.objects.filter(title=attrs['title']).exists():
            raise serializers.ValidationError({"error": "Task with this title already exists."})
        
        return super().validate(attrs)