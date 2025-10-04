from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=300, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='default.jpg')

    def __str__(self):
        return f"Profile - {self.user.username}"


# Signal runs every time a user object is saved.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

# Ensure that if you update a user, the related profile also gets saved.
# Keeps the User and Profile in sync
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

