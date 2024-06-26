from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.decorators import action, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from library.models import Genre, Book
from library.permissions.book_permissions import IsOwnerOrReadOnly
from library.permissions.genre_permissions import CanGetStatisticPermission
from library.serializers import (
    UserRegisterSerializer,
    GenreSerializer,
    BookSerializer
)
from library.utils.set_jwt import set_jwt_cookies


class BookDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BookListCreateView(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['GET'])
    # @permission_classes(CanGetStatisticPermission)
    def statistic(self, request, *args, **kwargs):
        genres_with_book_counts = Genre.objects.annotate(book_count=Count('books'))
        data = [
            {
                "id": genre.id,
                "genre": genre.name,
                "book_count": genre.book_count
            }
            for genre in genres_with_book_counts
        ]
        return Response(data)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request) -> Response:
        return Response(
            data={
                "message": "Hello, authentication user!!!",
                # "user": request.user.
            },
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        return Response(
            data={
                "message": "Data was created successfully"
            },
            status=status.HTTP_201_CREATED
        )


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user: User = serializer.save()

            response = Response(
                data={
                    "username": user.username,
                    "email": user.email if user.email else "No email"
                },
                status=status.HTTP_201_CREATED
            )

            set_jwt_cookies(response, user)

            return response

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user:

            response = Response(
                status=status.HTTP_200_OK,
            )

            set_jwt_cookies(response, user)

            return response

        else:
            return Response(
                data={
                    "message": 'Invalid credentials'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutUserView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
