from rest_framework import viewsets
from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer, CustomUserSerializer
from .models import Post, Comment, Like
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post_to_like = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check whether the user had already liked this post, to avoid duplication
    if Like.objects.filter(post= post_to_like, author=request.user):
        return Response (
            {
                'error': 'You already liked this post'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
    Like.objects.create(post=post_to_like, author=request.user)
    return Response(
        {'message': 'Liked post'},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    try:
        post_to_unlike = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response (
            {
                'error': 'Post not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        like_to_delete = Like.objects.get(post=post_to_unlike, author=request.user)
    except Like.DoesNotExist:
        return Response(
            {
                'message': 'You have not liked this post'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # delete the post
    like_to_delete.delete()
    return Response(
        {
            'message': 'You have unliked this post'
        },
        status=status.HTTP_200_OK
    )
    