from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from library.views import (
    ProtectedView,
    LoginUserView,
    LogoutUserView,
    RegisterUserView,
    GenreViewSet,
    BookListCreateView,
    BookDetailUpdateDeleteView,
)

genres_router = SimpleRouter()
books_router = DefaultRouter()

genres_router.register(r'', GenreViewSet, basename='genres')
books_router.register(r'', BookListCreateView, basename='books')

urlpatterns = [
    path('protected/', ProtectedView.as_view()),
    path('user-register/', RegisterUserView.as_view()),
    path('user-login/', LoginUserView.as_view()),
    path('user-logout/', LogoutUserView.as_view()),
    path('genres/', include(genres_router.urls)),
    path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view()),
    path('books/', include(books_router.urls)),
]
