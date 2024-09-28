from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification  # Make sure you have a Notification model
from django.shortcuts import get_object_or_404


User = get_user_model()


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
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')  # Correct the field name here


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
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Like a post."""
        # Use generics.get_object_or_404 to fetch the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Get or create a Like entry for this user and post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:  # If the Like already exists
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the like event
        Notification.objects.create(
            user=request.user,  # The user who performed the action
            post=post,  # The post being liked
            notification_type='like'  # Customize this field based on your Notification model
        )

        return Response({'detail': 'Post liked successfully!'}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Unlike a post."""
        # Use generics.get_object_or_404 to fetch the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Get the like object if it exists
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Like entry
        like.delete()

        # Optionally create a notification for the unlike event (if desired)
        Notification.objects.create(
            user=request.user,  # The user who performed the action
            post=post,  # The post being unliked
            notification_type='unlike'  # Customize this field based on your Notification model
        )

        return Response({'detail': 'Post unliked successfully!'}, status=status.HTTP_200_OK)




# from django.contrib.auth import get_user_model
# from django.shortcuts import render
# from rest_framework import generics, permissions
# from .models import Post  # Make sure you have a Post model
# from .serializers import PostSerializer, CommentSerializer # Assuming you have a serializer for posts
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Post, Comment
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Post, Like
# from .serializers import PostSerializer
# from notifications.models import Notification
# from django.shortcuts import get_object_or_404


# User = get_user_model()


# class FeedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Return posts from followed users, ordered by creation date."""
#         user = request.user
#         followed_users = user.following.all()
#         posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)



# class UserFeedView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         user = self.request.user
#         followed_users = user.following.all()
#         return Post.objects.filter(user__in=followed_users).order_by('-created_at')  # Assuming 'created_at' is the timestamp field

# # ViewSet for Post
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()  # Retrieve all posts
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]  # Only authenticated users can access

# # ViewSet for Comment
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()  # Retrieve all comments
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]  # Only authenticated users can access




# class LikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         """Like a post."""
#         post = get_object_or_404(Post, pk=pk)  # Use django.shortcuts.get_object_or_404

#         # Check if the user has already liked the post
#         if Like.objects.filter(user=request.user, post=post).exists():
#             return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Create a new Like entry
#         Like.objects.create(user=request.user, post=post)

#         # Optionally, you can create a notification here as well

#         return Response({'detail': 'Post liked successfully!'}, status=status.HTTP_201_CREATED)


# class UnlikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         """Unlike a post."""
#         post = get_object_or_404(Post, pk=pk)  # Use django.shortcuts.get_object_or_404

#         # Check if the user has liked the post
#         like = Like.objects.filter(user=request.user, post=post).first()
#         if not like:
#             return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Remove the Like entry
#         like.delete()

#         # Optionally, you can create a notification here as well

#         return Response({'detail': 'Post unliked successfully!'}, status=status.HTTP_200_OK)