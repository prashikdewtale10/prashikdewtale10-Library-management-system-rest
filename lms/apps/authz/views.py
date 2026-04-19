from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.authz.serializers import RegisterSerializer


# Create your views here.
class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "User register successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
