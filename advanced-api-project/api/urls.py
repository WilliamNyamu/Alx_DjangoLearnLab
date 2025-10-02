from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path("books/", views.ListView.as_view()),
    path("books/<int:pk>/", views.DetailView.as_view()),
    path("books/create/", views.CreateView.as_view()),
    path("books/update/", views.UpdateAPIView.as_view()),
    path("books/delete/", views.DeleteView.as_view()),
    path("api-auth/", include('rest_framework.urls'))
]