from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail

from library.models import Book

import cowsay


@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    if created:
        cowsay.beavis(f"NEW BOOK CREATED: {instance.title}")
    else:
        cowsay.beavis(f"THE BOOK IS UPDATED: {instance.title}")


def update_timestamp(sender, instance, **kwargs):
    instance.updated_at = timezone.now()


pre_save.connect(update_timestamp, sender=Book)


@receiver(post_save, sender=Book)
def notify_admin_on_new_book(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New book',
            'New book object was created. Please, check it.',
            'test.email@gmail.com',
            ['test.admin.py@gmail.com', 'django.creator@yahoo.com']
        )
