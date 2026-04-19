from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from apps.library.models import Book, BookReview
from apps.library.serializers import (
    BookReviewCreateSerializer,
    BookReviewDetailSerializer,
)


class ReviewAPIView(APIView):
    serializer_class = BookReviewCreateSerializer

    def get(self, request, id):
        book_reviews = BookReview.objects.filter(book=id)
        serializer = BookReviewDetailSerializer(book_reviews, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response(
                data={"message": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BookReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book, user=request.user)
            return Response(
                data={"message": "Review added successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
