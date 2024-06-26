from django.contrib.auth.models import User
from rest_framework import serializers

from library.models import Book, Genre, Publisher


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']


class AllBooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'title',
            'publisher',
            'published_date',
        )


class BookDetailSerializer(serializers.ModelSerializer):

    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'  # Включает все поля модели Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner']


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'published_date',
            'is_bestseller',
            'price'
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])

        user.save()

        return user
