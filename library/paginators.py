from rest_framework.pagination import CursorPagination


class PersonalCursorPaginator(CursorPagination):
    page_size = 10
    ordering = 'id'
