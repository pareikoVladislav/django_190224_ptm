from django.db import models
from django.core.validators import MaxValueValidator


GENRE_CHOICES = [
    ('Fiction', 'Fiction'),
    ('Non-Fiction', 'Non-Fiction'),
    ('Science Fiction', 'Science Fiction'),
    ('Fantasy', 'Fantasy'),
    ('Mystery', 'Mystery'),
    ('Biography', 'Biography'),
]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author_id = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)
    published_date = models.DateField()
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, related_name='books')
    publisher_id = models.ForeignKey('Member', related_name='books', null=True, on_delete=models.CASCADE)
    libraries = models.ManyToManyField('Library', related_name='books')
    summary = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, choices=GENRE_CHOICES)
    page_count = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)])

    @property
    def rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()

        if total_reviews == 0:
            return 0

        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews

        return round(average_rating, 2)

    def __str__(self):
        return self.title
