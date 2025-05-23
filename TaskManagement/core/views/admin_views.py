from rest_framework.views import APIView
from rest_framework.response import Response

class AdminPanal(APIView):
    def get(self,request):
        if request.method == 'GET':
            return Response({"message":"This is the admin panel"})