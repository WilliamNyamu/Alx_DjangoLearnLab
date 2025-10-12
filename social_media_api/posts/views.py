from rest_framework import viewsets
from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer, CustomUserSerializer
from .models import Post, Comment
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import permissions
# Create your views here.

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Attach the logged-in users as the author automatically."""
        serializer.save(author = self.request.user)

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Attach the logged-in users as the author automatically."""
        serializer.save(author=self.request.user)

class PostFeed(ListAPIView):
    serializer_class = PostSerializer
    ordering = ['-created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at').select_related('author')
        return queryset