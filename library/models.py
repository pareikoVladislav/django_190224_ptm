from django.contrib.auth.models import User
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    established_date = models.DateField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_get_statistic", "Can get genres statistic"),
        )


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        db_table = 'library_book'
        get_latest_by = 'published_date'
        default_related_name = 'books'
        unique_together = ('title', 'author')
        index_together = ('title', 'author')
