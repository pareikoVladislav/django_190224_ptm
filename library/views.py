from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from library.serializers import UserRegisterSerializer
from library.utils.set_jwt import set_jwt_cookies


# class ProtectedView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request: Request) -> Response:
#         return Response(
#             data={
#                 "message": "Hello, authentication user!!!",
#                 "user": request.user.username
#             },
#             status=status.HTTP_200_OK
#         )


class ProtectedView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            access_expiry = datetime.fromtimestamp(access_token['exp'])
            refresh_expiry = datetime.fromtimestamp(refresh['exp'])

            response = Response(
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=access_expiry
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )

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
