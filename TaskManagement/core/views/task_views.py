from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from core.models.task_models import Task
from core.models.user_models import User

from core.serializers.task_serializers import TaskSerializer ,ReportSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from core.permissions.permission import IsAdminOrSuperAdmin , IsAdmin , IsSuperAdmin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login




class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self,request):
        
        if request.user.role in ['admin','superadmin'] and request.user.is_active == True:
            all_tasks = Task.objects.filter(is_active=True)
        elif request.user.is_active == True:
            all_tasks = Task.objects.filter(is_active=True,assigned_to = request.user.id)  
        else:
            return Response({"error":"Only superadmins can view tasks."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(all_tasks,many = True)

        return Response(serializer.data)


class TaskListModification(APIView):
    permission_classes = [IsAuthenticated]

    
    
    def get(self,request,pk):
        if request.user.role in ['admin','superadmin'] and request.user.is_active == True:
            task =  get_object_or_404(Task,pk=pk,is_active=True)
        elif request.user.is_active == True:
            task =  get_object_or_404(Task,pk=pk,is_active=True,assigned_to = request.user.id)
        else:
            return Response({"error": "Only superadmins can view tasks."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        
        

    def post(self,request):
        if request.user.role in ['superadmin'] and request.user.is_active == True:
            serializer = TaskSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return  Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only superadmins can create tasks."}, status=status.HTTP_403_FORBIDDEN)

    def put(self,request,pk):
        if request.user.role in ['admin','superadmin'] and request.user.is_active == True:
            task = get_object_or_404(Task,pk=pk,is_active=True)
        
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.user.is_active == True:
            task = get_object_or_404(Task,pk=pk,assigned_to = request.user.id,is_active=True)
        
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Only superadmins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self,request,pk):
        data = request.data.copy()
        ALLOWED_FIELDS = {
                'superadmin': None,  # None = all allowed
                'admin': ['status', 'due_date', 'assigned_to'],
                'user': ['status', 'worked_hours'],
            }
        role = request.user.role

        if role in ['admin','superadmin'] and request.user.is_active == True:
            if role in ['admin'] and request.user.is_active == True:
                if ALLOWED_FIELDS[role] is not None:
                    data = {key: value for key, value in data.items() if key in ALLOWED_FIELDS[role]}
                    

            task = get_object_or_404(Task,pk=pk,is_active=True)
            

            
        elif role in ['user'] and request.user.is_active == True:
            task =  get_object_or_404(Task,pk=pk,is_active=True,assigned_to = request.user.id)
            if ALLOWED_FIELDS[role] is not None:
                    data = {key: value for key, value in data.items() if key in ALLOWED_FIELDS[role]}
                    
        else:
            return Response({"error": "Only superadmins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TaskSerializer(task, data=data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        if request.user.role in ['superadmin'] and request.user.is_active == True:
            task = get_object_or_404(Task,pk=pk,is_active=True)
            
            data = {
                'is_active': False
            }
            serializer = TaskSerializer(task, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only superadmins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
        
class TaskListReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request,pk):
        if request.user.role in ['admin','superadmin'] and request.user.is_active == True:
            
            all_tasks =  get_object_or_404(Task,pk=pk,is_active=True,status = 'completed')

        else:
            return Response({"error":"Only superadmins can view tasks."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReportSerializer(all_tasks)

        return Response(serializer.data)
    


#======================================================================================================================================================
