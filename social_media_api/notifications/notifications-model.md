Step-by-Step Explanation:
Step 1: Import Required Components
pythonfrom django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from rest_framework.authentication import get_user_model

User = get_user_model()
What's happening:

GenericForeignKey and ContentType allow the notification to point to any model (Post, Comment, Like, etc.)
get_user_model() gets your custom User model dynamically


Step 2: The recipient Field - Who Gets the Notification
pythonrecipient = models.ForeignKey(
    User, 
    related_name="notifications_received", 
    on_delete=models.CASCADE
)
What it does:

Stores who receives the notification
related_name="notifications_received" means you can do:

python  user.notifications_received.all()  # Get all notifications for this user
Example:

Alice likes Bob's post
recipient = Bob (he receives the notification)


Step 3: The actor Field - Who Triggered the Notification
pythonactor = models.ForeignKey(
    User, 
    related_name="notifications_sent", 
    on_delete=models.CASCADE
)
What it does:

Stores who performed the action that triggered the notification
related_name="notifications_sent" means you can do:

python  user.notifications_sent.all()  # Get all notifications this user caused
Example:

Alice likes Bob's post
actor = Alice (she performed the action)


Step 4: The verb Field - What Action Was Taken
pythonVERB_CHOICES = [
    ('like', 'liked your'),
    ('comment', 'commented on your'),
    ('follow', 'started following you'),
    ('mention', 'mentioned you in'),
    ('share', 'shared your'),
]
verb = models.CharField(max_length=50, choices=VERB_CHOICES)
What it does:

Stores what action was performed
Uses choices to limit valid values
First value ('like') is stored in database
Second value ('liked your') is the human-readable display

Usage:
pythonnotification.verb  # Returns: 'like'
notification.get_verb_display()  # Returns: 'liked your'
Example:

Alice likes Bob's post
verb = 'like'
Display: "Alice liked your post"


Step 5: The Generic Foreign Key - The Target Object (MOST IMPORTANT!)
python# Generic relation to any model (post, comment, etc.)
target_content_type = models.ForeignKey(
    ContentType, 
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
target_object_id = models.PositiveIntegerField(null=True, blank=True)
target = GenericForeignKey('target_content_type', 'target_object_id')
This is the magic! Let me explain in detail:
What is ContentType?
Django maintains a table of all models in your project:
ContentType Table:
+----+----------+-----------+
| id | app_label| model     |
+----+----------+-----------+
| 1  | blog     | post      |
| 2  | blog     | comment   |
| 3  | auth     | user      |
+----+----------+-----------+
How GenericForeignKey Works:
Instead of creating separate foreign keys for each model type:
python# ❌ You DON'T need this:
post = models.ForeignKey(Post, ...)
comment = models.ForeignKey(Comment, ...)
like = models.ForeignKey(Like, ...)
You use three fields together:

target_content_type: Stores WHICH model (Post, Comment, etc.)
target_object_id: Stores the ID of that object
target: The GenericForeignKey that combines both

Example in Database:
Notification Table:
+----+-------------+--------+--------+---------------------+------------------+
| id | recipient_id| actor_id| verb  | target_content_type | target_object_id |
+----+-------------+--------+--------+---------------------+------------------+
| 1  | 5 (Bob)     | 3(Alice)| like  | 1 (Post model)      | 10 (post id=10)  |
| 2  | 5 (Bob)     | 7(Carol)| comment| 2 (Comment model)   | 25 (comment id=25)|
| 3  | 5 (Bob)     | 3(Alice)| follow| NULL                | NULL              |
+----+-------------+--------+--------+---------------------+------------------+
Reading the table:

Row 1: Alice liked Bob's Post with id=10
Row 2: Carol commented on Bob's Comment with id=25
Row 3: Alice followed Bob (no target object needed)

Using the GenericForeignKey:
python# Creating notifications for different object types
from django.contrib.contenttypes.models import ContentType

# Notification for liking a POST
post = Post.objects.get(id=10)
Notification.objects.create(
    recipient=post.author,
    actor=request.user,
    verb='like',
    target=post  # Django automatically handles content_type and object_id!
)

# Notification for commenting (different model!)
comment = Comment.objects.get(id=25)
Notification.objects.create(
    recipient=comment.post.author,
    actor=request.user,
    verb='comment',
    target=comment  # Different model, same field!
)

# Notification for following (no target)
Notification.objects.create(
    recipient=user_to_follow,
    actor=request.user,
    verb='follow',
    target=None  # No target object
)
Accessing the Target:
pythonnotification = Notification.objects.first()

# Get the target object (could be Post, Comment, anything!)
target_object = notification.target

# Check what type it is
if isinstance(target_object, Post):
    print(f"This is about post: {target_object.title}")
elif isinstance(target_object, Comment):
    print(f"This is about comment: {target_object.text}")

# Or get the content type
content_type = notification.target_content_type
print(content_type.model)  # Prints: 'post' or 'comment' etc.

Step 6: Metadata Fields
pythonis_read = models.BooleanField(default=False)
timestamp = models.DateTimeField(auto_now_add=True)
What they do:

is_read: Track if user has seen the notification
timestamp: When the notification was created (auto-set)

Usage:
python# Mark notification as read
notification.is_read = True
notification.save()

# Get unread notifications
unread = user.notifications_received.filter(is_read=False)

Step 7: Meta Options
pythonclass Meta:
    ordering = ['-timestamp']  # Newest first
    indexes = [
        models.Index(fields=['recipient', '-timestamp']),  # Fast queries for user's notifications
        models.Index(fields=['recipient', 'is_read']),     # Fast queries for unread notifications
    ]
What they do:

ordering: Default sort order (newest first)
indexes: Speed up common queries (like "get Bob's unread notifications")


Step 8: The __str__ Method
pythondef __str__(self):
    return f"{self.actor.username} {self.get_verb_display()} - {self.recipient.username}"
Output examples:

"alice liked your - bob"
"carol commented on your - bob"
"alice started following you - bob"


Complete Real-World Example:
Scenario: Alice likes Bob's post
python# Step 1: Alice clicks like button
post = Post.objects.get(id=10)
post.author  # This is Bob

# Step 2: Create notification
notification = Notification.objects.create(
    recipient=post.author,      # Bob receives it
    actor=request.user,          # Alice did it
    verb='like',                 # The action
    target=post                  # The post being liked
)

# Behind the scenes, Django stores:
# - recipient_id = 5 (Bob's id)
# - actor_id = 3 (Alice's id)
# - verb = 'like'
# - target_content_type = ContentType for Post model
# - target_object_id = 10 (the post id)
# - is_read = False
# - timestamp = now()
How Bob Sees It:
python# Bob logs in and checks notifications
bob = User.objects.get(username='bob')
notifications = bob.notifications_received.filter(is_read=False)

for notif in notifications:
    print(f"{notif.actor.username} {notif.get_verb_display()} {notif.target}")
    # Output: "alice liked your Post: My awesome post"

Visual Flow:
Alice (actor) → [ACTION: like] → Bob's Post (target) → Bob (recipient) gets notification

Notification created:
┌─────────────────────────────────────────────┐
│ recipient: Bob                              │
│ actor: Alice                                │
│ verb: 'like'                                │
│ target: Post(id=10) ← GenericForeignKey     │
│ is_read: False                              │
│ timestamp: 2025-10-12 14:30:00             │
└─────────────────────────────────────────────┘

Why This Design Is Powerful:
✅ Flexible: Works with ANY model (Post, Comment, Like, Follow, etc.)
✅ Efficient: Only one Notification model needed
✅ Scalable: Easy to add new notification types
✅ Clean: No duplicate code for different notification types

Key Takeaways:

recipient: Who gets the notification
actor: Who caused the notification
verb: What action happened
target (GenericForeignKey): What object was acted upon (works with ANY model!)
is_read: Notification status
timestamp: When it happened

The GenericForeignKey is the secret sauce that makes this work for multiple model types! 🎯