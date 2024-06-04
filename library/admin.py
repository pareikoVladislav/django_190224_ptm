from django.contrib import admin
from django.utils import timezone

from library.models.book import Book
from library.models.member import Member
from library.models.author import Author
from library.models.category import Category
from library.models.library import Library


# class BookInline(admin.TabularInline):
#     model = Book
#     extra = 1

class BookInline(admin.StackedInline):
    model = Book
    extra = 1


class MemberAdmin(admin.ModelAdmin):
    inlines = [BookInline]


admin.site.register(Member, MemberAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_id', 'publisher_id', 'published_date', 'created_at')

    def update_created_at(modeladmin, request, queryset):
        queryset.update(created_at=timezone.now())

    update_created_at.short_description = "Update created_at to current time"

    actions = [update_created_at]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    ...
