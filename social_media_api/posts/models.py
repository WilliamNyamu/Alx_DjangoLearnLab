from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Set once when created: Post.objects.create()
    updated_at = models.DateTimeField(auto_now=True) # Set every time .save() is called

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}'s comment on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, related_name="posts_liked", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="authors_liked", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} liked {self.post}"
