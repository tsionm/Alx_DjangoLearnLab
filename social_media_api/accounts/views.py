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
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Like a post."""
        post = get_object_or_404(Post, pk=pk)

        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=request.user, post=post)
        return Response({'detail': 'Post liked successfully!'}, status=status.HTTP_201_CREATED)

# Unlike a post
class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Unlike a post."""
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
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

User = get_user_model()

# Follow a user
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Follow a user."""
        # Use CustomUser.objects.all() to emphasize the queryset
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        if request.user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follow(user_to_follow)
        return Response({'detail': 'User followed successfully'}, status=status.HTTP_200_OK)

# Unfollow a user
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Unfollow a user."""
        # Use CustomUser.objects.all() to emphasize the queryset.
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        if request.user == user_to_unfollow:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.unfollow(user_to_unfollow)
        return Response({'detail': 'User unfollowed successfully'}, status=status.HTTP_200_OK)