from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.library.models import BorrowRequest


@receiver(post_save, sender=BorrowRequest)
def update_book_copies_count(sender, instance, created, **kwargs):
    if created:
        return

    try:
        old_book_instance = BorrowRequest.objects.get(pk=instance.pk)
    except BorrowRequest.DoesNotExist:
        return

    book = instance.book

    if old_book_instance.status != "APPROVED" and instance.status == "APPROVED":
        book.availble_copies -= 1
        book.save()

    if old_book_instance.status != "RETURNED" and instance.status == "RETURNED":
        book.availble_copies += 1
        book.save()
