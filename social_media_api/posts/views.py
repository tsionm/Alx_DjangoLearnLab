from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post  # Make sure you have a Post model
from .serializers import PostSerializer, CommentSerializer # Assuming you have a serializer for posts
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment


class UserFeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(user__in=followed_users).order_by('-created_at')  # Assuming 'created_at' is the timestamp field

# ViewSet for Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # Retrieve all posts
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

# ViewSet for Comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # Retrieve all comments
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

# Create your views here.
