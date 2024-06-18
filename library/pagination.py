from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 2
    ordering = 'published_date'  # Укажите поле, которое существует в модели, например, 'published_date'
