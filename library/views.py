from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from library.models.book import Book
from library.serializers.books import AllBooksSerializer, BookSerializer, BookCreateSerializer


@api_view(['GET', 'POST'])
def simple_view(request: Request) -> Response:
    if request.method == 'GET':
        data = {'message': 'Hello World'}

        return Response(data)
    elif request.method == 'POST':
        data = {'message': 'THIS IS A POST REQUEST'}
        return Response(data)


@api_view(['GET',])
def get_all_books(request: Request) -> Response:
    books = Book.objects.all()

    if not books.exists():
        return Response(
            data=[],
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = AllBooksSerializer(books, many=True)

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET',])
def get_book_by_id(request: Request, book_id: int) -> Response:
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = BookSerializer(book)

    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST', ])
def create_new_book(request: Request) -> Response:
    serializer = BookCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT',])
def update_book_by_id(request: Request, book_id: int) -> Response:
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = BookCreateSerializer(book, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE',])
def delete_book_by_id(request: Request, book_id: int) -> Response:
    request.Get.get('genre')
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )

    book.delete()

    return Response(
        data={
            "message": "DELETED"
        },
        status=status.HTTP_200_OK
    )

# http://127.0.0.1:8000/api/v1/books/?status=YOUR%20CATEGORY&deadline=your%20awesome%20genre&page=3
