from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from core.models.task_models import Task
from core.serializers.task_serializers import TaskSerializer
from rest_framework import status


class TaskDetail(APIView):
    def get(self,request):
        
        all_tasks = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(all_tasks,many = True)

        return Response(serializer.data)


class TaskListModification(APIView):
    
    def get(self,request,pk):
        
        task =  get_object_or_404(Task,pk=pk,is_active=True)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        
        

    def post(self,request,pk):
        
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        
        task = get_object_or_404(Task,pk=pk)
    
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,pk):
        
        task = get_object_or_404(Task,pk=pk)
        

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        
        task = get_object_or_404(Task,pk=pk)
        
        data = {
            'is_active': False
        }
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        