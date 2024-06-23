from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from library.views import (
    BookListAPIView,
    GenreListRetrieveUpdateViewSet,
    CreateBookGenericView,
    # BookListReadOnlyVewSet,
    # BookListVewSet,
    # GenreListViewSet,
)

router = DefaultRouter()

router.register(r'genres', GenreListRetrieveUpdateViewSet)
# router.register(r'genres', GenreListViewSet)
# router.register(r'books-read-only', BookListReadOnlyVewSet, basename='books-read-only')
# router.register(r'books', BookListVewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('book-create/', CreateBookGenericView.as_view()),
    re_path(r'^books/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', BookListAPIView.as_view())
]
