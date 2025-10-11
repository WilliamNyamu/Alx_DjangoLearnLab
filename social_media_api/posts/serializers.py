from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'created_at', 'updated_at']
    
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.CharField(source='post.title')
    author = serializers.CharField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content']
    