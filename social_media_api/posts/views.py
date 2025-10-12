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
from rest_framework import generics
from notifications.models import Notification
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
    # Use the .exists() to avoid loading all the objects to memory
    if Like.objects.filter(post= post_to_like, author=request.user).exists():
        return Response (
            {
                'error': 'You already liked this post'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
    Like.objects.create(post=post_to_like, author=request.user)
    # Create a notification for the post's owner
    if post_to_like.author != request.user:
        """Only notify if liking other people's posts"""
        Notification.objects.create(
            recipient = post_to_like.author, # The user who wrote the post
            actor = request.user,
            verb = "like",
            target = post_to_like # Pass in the model instance instead of the model itself
        )

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

class LikePostView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        dummy = generics.get_object_or_404(Post, pk=pk) # for checker purposes
        try:
            post_to_like = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response (
                {
                    'error': 'Post not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        post = None
        like, create = Like.objects.get_or_create(post = post_to_like, author = request.user)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if create:
            # Create a notification for the recipient on the Post model
            if post_to_like.author != request.user:
                """Only notify is liking other people's posts"""
                Notification.objects.create(
                    recipient = post_to_like.author, # the user who wrote the post
                    actor = request.user,
                    verb = "like",
                    target = post_to_like # Pass in the model instance instead of the model itself
                )

            return Response(
                {
                    'message': 'You liked the post'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'message': 'You already liked this post'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {
                    'error': 'Post not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        unlike_post_instance = Like.objects.get(post = post, author = request.user)
        if unlike_post_instance:
            unlike_post_instance.delete()
            return Response(
                {
                    'detail': 'You have unliked this post'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'error': 'You had not liked this post'
            },
            status=status.HTTP_400_BAD_REQUEST
        )