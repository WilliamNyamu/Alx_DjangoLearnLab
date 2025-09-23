from django.urls import path, include
from .views import list_books, LibraryDetailView, register, login_view, logout_view, index
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns= [
    path("list_books/", list_books, name="list_books"),
    path("library_detail/", LibraryDetailView.as_view(), name="library_detail"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login" ),
    path("logout/", logout_view, name="logout"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("", index, name="index")
]