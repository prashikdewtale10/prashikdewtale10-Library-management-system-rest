from rest_framework import serializers

from apps.library.models import Author, Genre, Book, BookReview, BorrowRequest


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookListSerializers(serializers.ModelSerializer):
    # --- For getting author name ---
    author = serializers.StringRelatedField()
    genres = GenreSerializers(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookDetailSerializers(serializers.ModelSerializer):
    # --- Nested Serializers for other models data ---
    author = AuthorSerializer()
    genres = GenreSerializers(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = "__all__"


class BorrowRequestDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = BorrowRequest
        fields = "__all__"


class BookReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["rating", "comment"]


class BookReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()

    class Meta:
        model = BookReview
        fields = "__all__"
