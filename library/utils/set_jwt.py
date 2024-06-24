from datetime import datetime

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def set_jwt_cookies(response: Response, user) -> Response:
    # Создаем refresh токен для пользователя
    refresh_token = RefreshToken.for_user(user)
    # Получаем access токен из refresh токена
    access_token = refresh_token.access_token

    # Получаем время истечения access токена
    access_expiry = datetime.fromtimestamp(access_token['exp'])
    # Получаем время истечения refresh токена
    refresh_expiry = datetime.fromtimestamp(refresh_token['exp'])

    # Устанавливаем access токен в cookies
    response.set_cookie(
        key='access_token',  # Имя cookie
        value=str(access_token),  # Значение токена
        httponly=True,  # Запрет доступа к cookie через JavaScript
        secure=False,  # Использовать ли безопасное соединение (False для тестов)
        samesite='Lax',  # Политика SameSite для защиты от CSRF атак
        expires=access_expiry  # Время истечения cookie
    )
    # Устанавливаем refresh токен в cookies
    response.set_cookie(
        key='refresh_token',  # Имя cookie
        value=str(refresh_token),  # Значение токена
        httponly=True,  # Запрет доступа к cookie через JavaScript (строго http, https)
        secure=False,  # Использовать ли безопасное соединение (False для тестов)
        samesite='Lax',  # Политика SameSite для защиты от CSRF атак
        expires=refresh_expiry  # Время истечения cookie
    )

    # Возвращаем ответ с установленными cookies
    return response
