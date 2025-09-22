from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")
