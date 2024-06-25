from django.urls import path, include
from rest_framework.routers import SimpleRouter

from library.views import (
    ProtectedView,
    LoginUserView,
    LogoutUserView,
    RegisterUserView,
    GenreViewSet
)

genres_router = SimpleRouter()

genres_router.register(r'', GenreViewSet, basename='genres')

urlpatterns = [
    path('protected/', ProtectedView.as_view()),
    path('user-register/', RegisterUserView.as_view()),
    path('user-login/', LoginUserView.as_view()),
    path('user-logout/', LogoutUserView.as_view()),
    path('genres/', include(genres_router.urls)),
]
