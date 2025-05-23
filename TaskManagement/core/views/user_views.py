from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.user_models import User
from core.serializers.user_serializers import UserSerializer
from rest_framework import status


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class UserListView(APIView):
    def get(self, request):
        all_users = User.objects.filter(is_active=True)
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)
    
       



       