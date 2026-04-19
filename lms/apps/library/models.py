from django.db import models
from django.core.exceptions import ValidationError

from apps.authz.models import User


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ["name"]


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="books",
    )
    isbn = models.CharField(
        max_length=255,
        unique=True,
    )
    available_copies = models.IntegerField()
    total_copies = models.IntegerField()

    def __str__(self):
        return self.title

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError("Available copies cannot exceed total copies")


class BorrowRequest(models.Model):
    REQUEST_STATUS_CHOICES = (
        ("PENDING", "pending"),
        ("APPROVED", "approved"),
        ("REJECTED", "rejected"),
        ("RETURNED", "returned"),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrow_requests",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrow_requests",
    )
    status = models.CharField(
        max_length=10,
        choices=REQUEST_STATUS_CHOICES,
        default="PENDING",
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.user} - {self.book} - ({self.status})"


class BookReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="user_book_unique_review",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.book} - ({self.rating})"
