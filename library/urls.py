from django.urls import path

from library.views import (
    BookListGenericView,
    BookDetailGenericView,
    GenreDetailGenericView
)

urlpatterns = [
    path('books/', BookListGenericView.as_view()),
    path('books/<int:pk>/', BookDetailGenericView.as_view()),
    path('genres/<int:pk>/', GenreDetailGenericView.as_view()),
]
