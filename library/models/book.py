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
    created_at = models.DateTimeField(null=True, blank=True)
    is_bestseller = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

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


books = [
    Book(title='INFERNO', published_date='2009-07-25', genre='Fantasy', is_bestseller=True),
    Book(title='Da-Vinci Code', published_date='2011-05-30', genre='Fantasy', is_bestseller=True),
    Book(title='Test Book', published_date='2015-11-25'),
    Book(title='One mode book', published_date='2018-12-13', summary='TEST SUMMARY DESCRIPTION'),
]

books = Book.objects.all()

for book in books:
    book.price = Decimal('99.99')

Book.objects.bulk_update(books, ['price'])