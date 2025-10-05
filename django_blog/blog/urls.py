from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("", views.index, name="index")
]