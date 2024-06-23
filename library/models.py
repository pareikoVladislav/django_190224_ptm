from django.db import models
from django.utils import timezone

from library.managers import SoftDeleteManager


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    established_date = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, related_name='books')
    is_banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def __str__(self):
        return f"{self.title} by {self.author}"

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()

        self.save()

    class Meta:
        db_table = 'library_book'
        get_latest_by = 'published_date'
        default_related_name = 'books'
        unique_together = ('title', 'author')
        index_together = ('title', 'author')
