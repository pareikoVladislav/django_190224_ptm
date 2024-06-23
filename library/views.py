from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.db.models import Count

from library.models import Book, Genre
from library.serializers import BookSerializer, GenreSerializer
# from django.db import transaction
from rest_framework.decorators import action
# from rest_framework.generics import GenericAPIView, get_object_or_404
# from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import (
    # GenericViewSet,
    ReadOnlyModelViewSet,
    ModelViewSet
)


# 127.0.0.1:8000/api/v1/books/  GET POST
# 127.0.0.1:8000/api/v1/books/<book_id>/ GET PUT PATCH DELETE


# class CreateBookGenericView(GenericAPIView):
#     serializer_class = BookSerializer

    # def create_new_book_action(self, book):
    #     print(f"\n{'=' * 50} Book '{book.title}' created successfully {'=' * 50}\n")
    #
    # def post(self, request, *args, **kwargs):
    #     try:
    #         with transaction.atomic():
    #             publisher = Publisher.objects.create(
    #                 name='TEST Publisher',
    #                 established_date='2024-06-19'
    #             )
    #
    #             book = Book.objects.create(
    #                 title='MY TEST BOOK',
    #                 author='R. L. Stain22',
    #                 published_date='2024-06-19',
    #                 publisher=publisher
    #             )
    #
    #             transaction.on_commit(
    #                 lambda: self.create_new_book_action(book)
    #             )
    #
    #             serializer = self.serializer_class(book)
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(
    #             {"error": str(e)},
    #             status.HTTP_400_BAD_REQUEST
    #         )

    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    #     try:
    #         with transaction.atomic():
    #             publisher = Publisher.objects.create(
    #                 name='TRANSACTION Publisher',
    #                 established_date='2024-06-19'
    #             )
    #
    #             book = Book.objects.create(
    #                 title='TRANSACTION BOOK',
    #                 author='TRANSACTION Stain',
    #                 published_date='2024-06-20',
    #                 publisher=publisher
    #             )
    #
    #             if Publisher.objects.filter(name="TRANSACTION Publisher").count() > 1:
    #                 transaction.set_rollback(True)
    #
    #             serializer = self.serializer_class(book)
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(
    #             {"error": str(e)},
    #             status.HTTP_400_BAD_REQUEST
    #         )


# class GenreListRetrieveUpdateViewSet(mixins.ListModelMixin,
#                                      mixins.RetrieveModelMixin,
#                                      mixins.UpdateModelMixin,
#                                      viewsets.GenericViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#

class GenreListViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=False, methods=['GET'])
    def statistic(self, request: Request) -> Response:
        genres = Genre.objects.annotate(
            book_count=Count('books')
        )

        data = [
            {
                'id': genre.id,
                'genre': genre.name,
                'book_count': genre.book_count
            }
            for genre in genres
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class BookListReadOnlyVewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListVewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListAPIView(APIView):
    serializer_class = BookSerializer

    # queryset = Book.objects.all()

    def get_objects(self, year, month, day):
        books = Book.objects.filter(
            published_date__year=year,
            published_date__month=month,
            published_date__day=day
        )

        return books

    def get(self, request: Request, *args, **kwargs) -> Response:
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']

        books = self.get_objects(year, month, day)

        if not books.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.serializer_class(books, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
