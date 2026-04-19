from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.paginator import Paginator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.library.models import Book
from apps.library.serializers import (
    BookListSerializers,
    BookDetailSerializers,
    BookCreateUpdateSerializer,
)
from apps.library.permissions import IsLibrarian


class BookAPIView(APIView):
    serializer_class = BookCreateUpdateSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author__name", "genres__name"]
    orderning_fields = ["title", "available_copies", "total_copies"]

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsLibrarian()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):

        # --- Get book by book id ---
        books = Book.objects.select_related("author").prefetch_related("genres")
        books = books.distinct()

        title = request.query_params.get("title")
        author = request.query_params.get("author")
        genre = request.query_params.get("genre")

        # --- Filtering books by title/author/genre ---
        if title:
            books = books.filter(title__icontains=title)

        if author:
            books = books.filter(author__name__icontains=author)

        if genre:
            books = books.filter(genres__name__icontains=genre)

        for backend in list(self.filter_backends):
            books = backend().filter_queryset(request, books, self)

        # --- Pagination ---
        page = int(request.query_params.get("page", 1))
        page_size = min(int(request.query_params.get("page_size", 5)), 50)

        paginator = Paginator(books, page_size)
        page_obj = paginator.get_page(page)

        serializer = BookListSerializers(page_obj, many=True)
        return Response(
            {
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "results": serializer.data,
            }
        )

    def post(self, request):
        serializer = BookCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Book added successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    serializer_class = BookCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsLibrarian()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
            serializer = BookDetailSerializers(book)  # Use your detail serializer
            return Response(data=serializer.data)
        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=404)

    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response(
                data={"message": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BookCreateUpdateSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "Book updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response(
                data={"message": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        book.delete()
        return Response(data={"message": "Book updated successfully."})
