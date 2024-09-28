from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# class User(AbstractUser):
#     following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

#     def follow(self, user):
#         """Follow another user."""
#         if user != self:
#             self.following.add(user)

#     def unfollow(self, user):
#         """Unfollow another user."""
#         if user != self:
#             self.following.remove(user)

#     def is_following(self, user):
#         """Check if the user is following another user."""
#         return self.following.filter(id=user.id).exists()

#     def is_followed_by(self, user):
#         """Check if the user is followed by another user."""
#         return self.followers.filter(id=user.id).exists()
class CustomUser(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def follow(self, user):
        """Follow another user."""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user."""
        self.following.remove(user)


# class CustomUser(AbstractUser):

#     groups = models.ManyToManyField(
#         Group,
#         related_name="customuser_groups",  # Add this to resolve clash
#         blank=True,
#         help_text="The groups this user belongs to.",
#         verbose_name="groups",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="customuser_user_permissions",  # Add this to resolve clash
#         blank=True,
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions",
#     )

#     def __str__(self):
#         return self.username



# # Create your models here.
