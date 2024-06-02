from django.db import models
from django.utils import timezone


class Borrow(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='borrows')
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def is_overdue(self):
        if self.returned:
            return False
        return self.return_date < timezone.now().date()
