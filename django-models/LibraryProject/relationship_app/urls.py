from django.urls import path
from . import views

urlpatterns= [
    path("list_books", views.list_books, name="list_books"),
    path("library_detail", views.LibraryView.as_view(), name="library_detail")
]