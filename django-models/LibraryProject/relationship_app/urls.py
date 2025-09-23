from django.urls import path, include
from .views import list_books, LibraryDetailView, SignUpView

urlpatterns= [
    path("list_books/", list_books, name="list_books"),
    path("library_detail/", LibraryDetailView.as_view(), name="library_detail"),
    path("signup/", SignUpView, name="signup"),
    path("accounts/", include('django.contrib.auth.urls'))
]