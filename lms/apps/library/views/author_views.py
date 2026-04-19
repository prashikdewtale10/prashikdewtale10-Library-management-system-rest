from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from apps.library.models import Author
from apps.library.serializers import AuthorSerializer
from apps.library.permissions import IsLibrarian


class AuthorAPIView(APIView):
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsLibrarian()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
