from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets
# Create your views here.

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
