from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at')
    body = models.TextField()
    author = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='posts')
    moderated = models.BooleanField(default=False)
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateField()
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
