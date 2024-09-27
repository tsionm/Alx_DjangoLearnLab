from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post  # Make sure you have a Post model
from .serializers import PostSerializer  # Assuming you have a serializer for posts

class UserFeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(user__in=followed_users).order_by('-created_at')  # Assuming 'created_at' is the timestamp field
# Create your views here.
