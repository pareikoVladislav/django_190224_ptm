from django.urls import path

from library.views import (
    ProtectedView,
    LoginUserView,
    LogoutUserView,
    RegisterUserView
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('protected/', ProtectedView.as_view()),
    path('user-register/', RegisterUserView.as_view()),
    path('user-login/', LoginUserView.as_view()),
    path('user-logout/', LogoutUserView.as_view()),
    # path('auth-token/', obtain_auth_token),
    # path('jwt-auth/', TokenObtainPairView.as_view()),
    # path('jwt-refresh/', TokenRefreshView.as_view()),
]
