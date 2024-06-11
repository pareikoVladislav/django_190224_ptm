from rest_framework import serializers

from library.models.book import Book
from library.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AllBooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'title',
            'publisher_id',
            'published_date',
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'author_id',
            'published_date',
            'is_bestseller',
            'price'
        )
