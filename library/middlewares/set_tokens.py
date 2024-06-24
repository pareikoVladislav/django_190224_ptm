from datetime import datetime
from rest_framework.request import Request
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: Request, **kwargs):
        # Получаем access токен и refresh токен из cookies
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Если access_token получен, всё хорошо:
        if access_token:
            try:
                # Декодируем access токен
                token = AccessToken(access_token)
                # Проверяем истечение срока действия токена
                if datetime.fromtimestamp(token['exp']) < datetime.now():
                    raise TokenError('Token is expired')
                # Добавляем токен в заголовки запроса
                request.META['HTTP_AUTHORIZATION'] = f"JWT {access_token}"

            except TokenError:
                # Обновляем access токен при ошибке
                new_access_token = self.refresh_access_token(refresh_token)

                # если смогли обновить access_token
                if new_access_token:
                    # Добавляем новый токен в заголовки
                    request.META['HTTP_AUTHORIZATION'] = f"JWT {new_access_token}"

                    # Сохраняем новый токен в запрос
                    request._new_access_token = new_access_token

                # в противном случае
                else:
                    # Очищаем cookies, если обновление не удалось
                    self.clear_cookies(request)

        # так же если не access_token, а refresh_token:
        elif refresh_token:
            # Обновляем access токен по refresh токену
            new_access_token = self.refresh_access_token(refresh_token)

            if new_access_token:
                # Добавляем новый токен в заголовки
                request.META['HTTP_AUTHORIZATION'] = f"JWT {new_access_token}"

                # Сохраняем новый токен в запрос
                request._new_access_token = new_access_token

            else:
                # Очищаем cookies, если обновление не удалось
                self.clear_cookies(request)

    def process_response(self, request: Request, response: Response, **kwargs):
        # Получаем новый токен из запроса
        new_access_token = getattr(request, '_new_access_token', None)

        if new_access_token:
            # Получаем время истечения нового токена
            access_expiry = AccessToken(new_access_token)['exp']
            response.set_cookie(
                key='access_token',  # Имя cookie
                value=new_access_token,  # Значение нового токена
                httponly=True,  # Запрет доступа к cookie через JavaScript
                secure=False,  # Использовать ли безопасное соединение (False для тестов)
                samesite='Lax',  # Политика SameSite для защиты от CSRF атак
                expires=datetime.fromtimestamp(access_expiry)  # Время истечения cookie
            )
        # Возвращаем ответ с установленными cookies
        return response

    def refresh_access_token(self, refresh_token):
        try:
            # Создаем новый refresh токен
            refresh = RefreshToken(refresh_token)
            # Получаем новый access токен из refresh токена
            new_access_token = str(refresh.access_token)

            # Возвращаем новый access токен
            return new_access_token
        except TokenError:
            # Возвращаем None при ошибке
            return None

    def clear_cookies(self, request: Request):
        request.COOKIES.pop('access_token', None)  # Удаляем access токен из cookies
        request.COOKIES.pop('refresh_token', None)  # Удаляем refresh токен из cookies
