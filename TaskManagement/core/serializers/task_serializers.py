from rest_framework import serializers
from core.models.task_models import Task




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'assigned_to', 'worked_hours', 'completion_report', 'is_active', 'created_at', 'updated_at']  

    
    def validate(self, attrs):
        request = self.context.get('request')
        method = getattr(request, 'method', None)

        title = attrs.get('title')
        status = attrs.get('status')
        completion_report = attrs.get('completion_report')
        worked_hours = attrs.get('worked_hours')

        # Check empty title
        if title is not None and title.strip() == '':
            raise serializers.ValidationError({"title": "Title cannot be empty."})

        # Unique title check for POST
        if method == 'POST' and title and Task.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title": "Task with this title already exists."})

        # Completed status checks
        if status == 'completed':
            if not completion_report or len(completion_report.split()) < 10:
                raise serializers.ValidationError({
                    "completion_report": "Must be at least 10 words for completed tasks."
                })
            if worked_hours is None or worked_hours <= 1.0:
                raise serializers.ValidationError({
                    "worked_hours": "Must be greater than 1 hour for completed tasks."
                })

        return super().validate(attrs)











    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'worked_hours', 'completion_report']