from django.urls import path
from . import views

urlpatterns = [
    # Auth routes
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    # Crud operations
    path("posts/", views.PostsView.as_view(), name="posts"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("post/<int:post_pk>/comment/<int:comment_pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("post/<int:post_pk>/comments/<int:comment_pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path('tags/<slug:tag_name>/', views.PostsByTagView.as_view(), name='posts-by-tag'),
    path('search/', views.search_view, name='search'),
    path("comment/<int:pk>/comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view()),
    path("", views.index, name="index")
]