from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.models import Post, Like  # Assuming posts and likes are in the 'posts' app
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()

# Like a post
class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Like a post."""
        # Fetch the post using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Get or create a Like entry for this user and post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:  # If the Like already exists
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the like event
        Notification.objects.create(
            user=request.user,  # The user who performed the action
            post=post,  # The post being liked
            notification_type='like'  # Customize this field as per your notification logic
        )

        return Response({'detail': 'Post liked successfully!'}, status=status.HTTP_201_CREATED)

# Unlike a post
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Unlike a post."""
        # Fetch the post using generics.get_object_or_404
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
            notification_type='unlike'  # Customize this field as per your notification logic
        )

        return Response({'detail': 'Post unliked successfully!'}, status=status.HTTP_200_OK)

# User registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Follow a user
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can follow

    def post(self, request, user_id):
        """Follow a user."""
        # Fetch the user to follow from the list of all users
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        # Check to ensure that users can't follow themselves
        if request.user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already following this user
        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the follow action
        request.user.follow(user_to_follow)
        return Response({'detail': 'User followed successfully'}, status=status.HTTP_200_OK)

# Unfollow a user
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can unfollow

    def post(self, request, user_id):
        """Unfollow a user."""
        # Fetch the user to unfollow from the list of all users
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        # Check to ensure that users can't unfollow themselves
        if request.user == user_to_unfollow:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is currently following the user
        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the unfollow action
        request.user.unfollow(user_to_unfollow)
        return Response({'detail': 'User unfollowed successfully'}, status=status.HTTP_200_OK)