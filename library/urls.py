from django.urls import path

from library.views import (
    simple_view,
    get_all_books,
    get_book_by_id,
    create_new_book,
    update_book_by_id,
    delete_book_by_id
)

urlpatterns = [
    path('', simple_view),
    path('books/', get_all_books),
    path('books/<int:book_id>/', get_book_by_id),
    path('books/create/', create_new_book),
    path('books/<int:book_id>/update/', update_book_by_id),
    path('books/<int:book_id>/delete/', delete_book_by_id),
]
