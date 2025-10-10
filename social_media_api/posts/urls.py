from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListAPIView.as_view(), name="posts"),
    path("comments/", views.CommentListAPIView.as_view(), name="comments")
]