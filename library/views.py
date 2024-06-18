from rest_framework.generics import (
    GenericAPIView,
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import (
#     PageNumberPagination,
#     LimitOffsetPagination,
#     CursorPagination
# )

from library.models import Book, Genre, Publisher
from library.serializers import (
    BookSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    GenreSerializer
)


class GenreDetailGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_object(self):
        genre = get_object_or_404(Genre, pk=self.kwargs['pk'])

        return genre


class BookDetailGenericView(GenericAPIView):
    queryset = Book.objects.all()

    # serializer_class = BookDetailGenericView

    def get_object(self):
        # pk = self.kwargs.get('pk')
        # try:
        #     return Book.objects.get(pk=self.kwargs['pk'])
        #
        # except Book.DoesNotExist:
        #     return Response(
        #         data={},
        #         status=status.HTTP_204_NO_CONTENT
        #     )

        return get_object_or_404(Book, pk=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookDetailSerializer

        elif self.request.method == "PUT":
            return BookCreateSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        book = self.get_object()

        serializer = self.get_serializer(book)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        book = self.get_object()

        serializer = self.get_serializer(
            instance=book,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        book = self.get_object()

        book.delete()

        return Response(
            data={
                "message": "The book has been deleted."
            },
            status=status.HTTP_204_NO_CONTENT
        )


class BookListGenericView(ListCreateAPIView):
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer

    def get_queryset(self, *args, **kwargs):
        author = self.request.query_params.get('author')

        if author:
            queryset = Book.objects.filter(author=author)

            return queryset

        return Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookSerializer

        return BookCreateSerializer

# class BookPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = "page_size"
#     max_page_size = 4
#
#
# class BookCursorPagination(CursorPagination):
#     page_size = 2
#     ordering = "published_date"
#
#
# class BookListGenericView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     pagination_class = BookCursorPagination


# class BookListGenericView(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['author', 'is_bestseller']
#     search_fields = ['title', 'author']
#     ordering_fields = ['published_date', 'price']

# def get_queryset(self, *args, **kwargs):
#     # queryset = Book.objects.all()
#     #
#     # author = self.request.query_params.get('author')
#     #
#     # if author:
#     #     queryset = queryset.filter(author=author)
#     #
#     # return queryset
#     # pk = self.kwargs['pk']
#     author = self.request.query_params.get('author')
#
#     if author:
#         queryset = Book.objects.filter(author=author)
#
#         return queryset
#
#     return Book.objects.all()

# def get_serializer_context(self):
#     context = super().get_serializer_context()
#     context['include_related'] = self.request.query_params.get(
#         'include_related', 'false').lower() == 'true'
#
#     return context
#
# def get_serializer_class(self):
#     if self.request.method == "GET":
#         return BookSerializer
#
#     return BookCreateSerializer
#
# def list(self, request: Request, *args, **kwargs) -> Response:
#     books = self.get_queryset()
#
#     if not books.exists():
#         return Response(
#             data=[],
#             status=status.HTTP_204_NO_CONTENT
#         )
#
#     serializer = self.get_serializer(books, many=True)
#
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )
#
# def create(self, request: Request, *args, **kwargs) -> Response:
#     data = request.data.copy()
#
#     if 'author' not in data or not data['author']:
#         data['author'] = 'Unknown Author'
#
#     serializer = self.get_serializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     self.perform_create(serializer)
#
#     return Response(
#         serializer.data,
#         status=status.HTTP_201_CREATED
#     )


# def get(self, request: Request, *args, **kwargs) -> Response:
#     books = self.get_queryset(*args, **kwargs)
#
#     if not books.exists():
#         return Response(
#             data=[],
#             status=status.HTTP_204_NO_CONTENT
#         )
#
#     serializer = self.get_serializer(books, many=True)
#
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )
#
# def post(self, request: Request, *args, **kwargs) -> Response:
#     serializer = self.get_serializer(data=request.data)
#
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED
#         )
#
#     return Response(
#         data=serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )
