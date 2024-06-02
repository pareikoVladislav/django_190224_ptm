from django.db import models


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.book} - {self.reviewer} - {self.rating}"
