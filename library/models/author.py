from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from library.models.member import GENDER_CHOICES


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    profile = models.URLField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.first_name


class AuthorDetail(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='details')
    biography = models.TextField()
    birth_city = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
