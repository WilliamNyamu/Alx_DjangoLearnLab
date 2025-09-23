from django.urls import path, include
from .views import list_books, LibraryDetailView, register, login_view, logout_view, index

urlpatterns= [
    path("list_books/", list_books, name="list_books"),
    path("library_detail/", LibraryDetailView.as_view(), name="library_detail"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login" ),
    path("logout/", logout_view, name="logout"),
    path("", index, name="index")
]