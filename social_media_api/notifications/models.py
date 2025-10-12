from django.db import models
from rest_framework.authentication import get_user_model

User = get_user_model()

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=300)
    target = models.ForeignKey('self', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)