from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from rest_framework.authentication import get_user_model

User = get_user_model()

class Notification(models.Model):
    # Who receives this notification
    recipient = models.ForeignKey(
        User, 
        related_name="notifications_received", 
        on_delete=models.CASCADE
    )
    
    # Who triggered this notification
    actor = models.ForeignKey(
        User, 
        related_name="notifications_sent", 
        on_delete=models.CASCADE
    )
    
    # What action was taken
    VERB_CHOICES = [
        ('like', 'liked your'),
        ('comment', 'commented on your'),
        ('follow', 'started following you'),
        ('mention', 'mentioned you in'),
        ('share', 'shared your'),
    ]
    verb = models.CharField(max_length=50, choices=VERB_CHOICES)
    
    # Generic relation to any model (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    # Metadata
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()} - {self.recipient.username}"