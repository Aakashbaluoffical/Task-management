from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.user_models import User
from core.serializers.user_serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role in ['superadmin'] and request.user.is_active == True:
            all_users = User.objects.filter(is_active=True)
            serializer = UserSerializer(all_users, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Only superadmins can view users."}, status=status.HTTP_403_FORBIDDEN)
    
       



       