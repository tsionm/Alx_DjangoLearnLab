from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post  # Make sure you have a Post model
from .serializers import PostSerializer, CommentSerializer # Assuming you have a serializer for posts
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return posts from followed users, ordered by creation date."""
        user = request.user
        followed_users = user.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)



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




class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:  # New like
            # Create a notification
            notification = Notification.objects.create(
                recipient=post.author,  # Assuming Post has an author field
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Post already liked.'}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'detail': 'Post unliked.'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'detail': 'Post not liked.'}, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
