from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostView, basename="posts")
router.register(r'comments', views.CommentView, basename="comments")

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.PostFeed.as_view(), name="feed"),
    path('posts/<int:post_id>/like/', views.like_post, name="like"),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name="unlike"),
]