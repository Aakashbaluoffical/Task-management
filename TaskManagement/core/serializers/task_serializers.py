from rest_framework import serializers
from core.models.task_models import Task




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'assigned_to', 'worked_hours', 'completion_report', 'is_active', 'created_at', 'updated_at']  

    def validate(self, attrs):
        request = self.context.get('request')
        method = request.method if request else None
        
        if 'title' in attrs and not attrs['title']:
            raise serializers.ValidationError({"error": "Title is empty"})
        
        if method == 'POST':    
            if attrs.get('title') and Task.objects.filter(title=attrs['title']).exists():
                raise serializers.ValidationError({"error": "Task with this title already exists."})
        
        if attrs.get('status') == 'completed' and  attrs.get('completion_report') == None and attrs.get('worked_hours') == None:
            raise serializers.ValidationError({"error": "Completion report and worked_hours are required for completed tasks."})
        return super().validate(attrs)
    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'worked_hours', 'completion_report']