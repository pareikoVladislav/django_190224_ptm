from django.contrib import admin
from django.utils import timezone

from library.models import Book, Publisher, Genre


class BookInline(admin.StackedInline):
    model = Book
    extra = 1


class MemberAdmin(admin.ModelAdmin):
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'published_date', 'created_at')

    def update_created_at(modeladmin, request, queryset):
        queryset.update(created_at=timezone.now())

    update_created_at.short_description = "Update created_at to current time"

    actions = [update_created_at]


admin.site.register(Publisher)
admin.site.register(Genre)
