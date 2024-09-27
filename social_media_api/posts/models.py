# posts/models.py

from django.db import models
from accounts.models import CustomUser  # Import your custom user model

class Post(models.Model):
    # ForeignKey linking the post to a user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    # Text content of the post
    content = models.TextField()
    # Automatically set the date and time the post was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation for easy identification of posts in admin or shell
        return f'Post by {self.user.username}: {self.content[:20]}'

class Comment(models.Model):
    # ForeignKey linking the comment to a post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # ForeignKey linking the comment to a user
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Text content of the comment
    content = models.TextField()
    # Automatically set the date and time the comment was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation for easy identification of comments
        return f'Comment by {self.user.username} on {self.post.id}: {self.content[:20]}'
