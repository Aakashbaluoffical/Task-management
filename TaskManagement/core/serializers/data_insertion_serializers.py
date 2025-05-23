from rest_framework import serializers
from core.models.task_models import Task
from core.models.user_models import User
from rest_framework.response import Response



class TaskDataUpload(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = ['id', 'title', 'description', 'due_date', 'worked_hours', 'completion_report', 'is_active', 'status']

        
    def validate(self, attrs):
        print("========",attrs)
        if not attrs['title']:
            raise Response({"error": "Title is empty"}, status=400)
        if not attrs['description']:
            raise Response({"error": "Description is empty"}, status=400)
        if not attrs['due_date']:
            raise Response({"error": "Due date is empty"}, status=400)
        
        if not attrs['worked_hours']:
            raise Response({"error": "Worked hours is empty"}, status=400)
        
        if 'is_active' not in attrs:
            raise Response({"error": "is_active is empty"}, status=400)
        if not attrs['status']:
            raise Response({"error": "Status is empty"}, status=400)

        return super().validate(attrs)

class UserDataUpload(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','password','role','is_active']
        


    def validate(self, attrs):

        if not attrs['username']:
            raise Response({"error": "Username is empty"}, status=400)
        if not attrs['role']:
            raise Response({"error": "Role is empty"}, status=400)
        if not attrs['password']:
            raise Response({"error": "Password is empty"}, status=400)
        if 'is_active' not in attrs:
            
            raise Response({"error": "is_active is empty"}, status=400)

        if  User.objects.filter(username=attrs['username']).exists():
            raise Response({"error": "User already exists"}, status=400)

        return super().validate(attrs)