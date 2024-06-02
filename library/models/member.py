from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Staff', 'Staff'),
    ('Reader', 'Reader'),
]


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    active = models.BooleanField(default=True)
    libraries = models.ManyToManyField('Library', related_name='members')

    def __str__(self):
        return f'{self.first_name} {self.last_name[0]}.'
