from django.contrib import admin

from .models import Author, Genre, Book, BookReview, BorrowRequest


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    list_display = ["name"]


class GenreAdmin(admin.ModelAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    list_display = ["name"]


class BookAdmin(admin.ModelAdmin):
    ordering = ["title"]
    search_fields = ["title", "author__name", "genres__name", "isbn"]
    list_display = ["title", "author", "isbn"]
    list_filter = ["author", "genres"]
    list_select_related = ["author"]

    class Meta:
        orderning = ["title"]


class BorrowRequestAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "book__title"]
    list_display = ["user", "book", "status", "requested_at"]
    list_filter = ["status"]


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "book__title"]
    list_display = ["user", "book", "rating", "created_at"]
    list_filter = ["rating"]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowRequest, BorrowRequestAdmin)
admin.site.register(BookReview, BookReviewAdmin)
