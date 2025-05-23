from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models.task_models import Task
from core.models.user_models import User
# from core.serializers.data_insertion_serializers import TaskDataUpload, UserDataUpload
from core.serializers.task_serializers import TaskSerializer
from core.serializers.user_serializers import UserSerializer

from rest_framework import status

import csv
import io

@api_view(['POST'])
def insert_data(request,table_name:str):
    if not table_name:
        return Response({'error':'No table name provided'}, status=400)
    
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=400)
    
    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return Response({"error": "File is not a CSV"}, status=400)
    
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    data = csv.DictReader(io_string)

    if table_name == 'Task':
        # Assuming the Task model has fields: id, title, description, status
        for row in data:
            print("========",row)
            # del row['assigned_to']

            serializer = TaskSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
            
        
            

        return Response({'message': 'Task data inserted successfully'}, status=201)
        
    elif table_name == 'User':
        # Assuming the User model has fields: id, name, email
        for row in data:
            print("===========",row)
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
                
        return Response({'message': 'Task data inserted successfully'}, status=201)
        
    else:
        return Response({'error':'Invalid table name'},status=400)
    



        







