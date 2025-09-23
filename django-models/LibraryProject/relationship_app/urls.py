from django.urls import path
from .views import LibraryView, list_books

urlpatterns= [
    path("list_books", list_books, name="list_books"),
    path("library_detail", LibraryView.as_view(), name="library_detail")
]