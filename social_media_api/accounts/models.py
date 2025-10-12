from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    """ Adding other fields for the User model """
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/',blank=True, null=True)
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, # Following is not mutual! If I follow someone, that doesn't mean that they automatically follow me
        related_name= "followers",
        blank=True
    )



