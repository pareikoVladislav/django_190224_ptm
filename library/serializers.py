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

    def to_representation(self, instance):
        # Использование параметра include_related из контекста
        representation = super().to_representation(instance)
        if self.context.get('include_related'):
            representation['genres'] = [genre.name for genre in instance.genres.all()]
        else:
            representation.pop('genres', None)
        return representation


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
