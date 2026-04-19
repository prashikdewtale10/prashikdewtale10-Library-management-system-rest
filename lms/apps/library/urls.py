from django.urls import path

from apps.library.views.genre_views import GenreAPIView
from apps.library.views.author_views import AuthorAPIView
from apps.library.views.book_views import BookAPIView, BookDetailAPIView
from apps.library.views.review_views import ReviewAPIView

urlpatterns = [
    # --- Author API URLs ---
    path("authors/", AuthorAPIView.as_view(), name="author-list-create"),
    # --- Genre API URLs ---
    path("genres/", GenreAPIView.as_view(), name="genre-list-create"),
    # --- Book Review API URLs ---
    path(
        "books/<int:id>/reviews/",
        ReviewAPIView.as_view(),
        name="book-reviews-list-create",
    ),
    # --- Book API URLs ---
    path("books/", BookAPIView.as_view(), name="books-list-create"),
    path("books/<int:id>", BookDetailAPIView.as_view(), name="book-detail"),
]
