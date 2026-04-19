from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from apps.library.models import Genre
from apps.library.serializers import GenreSerializers
from apps.library.permissions import IsLibrarian


class GenreAPIView(APIView):
    serializer_class = GenreSerializers

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsLibrarian()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializers(genres, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = GenreSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Genre added successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
