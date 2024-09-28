from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser  # Ensure your CustomUser model is imported
from .serializers import UserSerializer  # Import your user serializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.permissions import IsAuthenticated
# from .models import Post, Like
from posts.models import Post, Like
from django.contrib.auth import get_user_model


User = get_user_model()

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Like a post."""
        post = get_object_or_404(Post, pk=pk)
        
        # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Like entry
        Like.objects.create(user=request.user, post=post)
        
        # Optionally, you can create a notification here as well

        return Response({'detail': 'Post liked successfully!'}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Unlike a post."""
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the Like entry
        like.delete()

        # Optionally, you can create a notification here as well

        return Response({'detail': 'Post unliked successfully!'}, status=status.HTTP_200_OK)





class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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



# class FollowUserView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = CustomUser.objects.all()
    
#     def update(self, request, *args, **kwargs):
#         user_to_follow = self.get_object()
#         request.user.following.add(user_to_follow)  # Add user to following
#         return Response({'status': 'user followed'}, status=status.HTTP_200_OK)

# class UnfollowUserView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = CustomUser.objects.all()
    
#     def update(self, request, *args, **kwargs):
#         user_to_unfollow = self.get_object()
#         request.user.following.remove(user_to_unfollow)  # Remove user from following
#         return Response({'status': 'user unfollowed'}, status=status.HTTP_200_OK)
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Follow a user."""
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        request.user.follow(user_to_follow)
        return Response({'detail': 'User followed successfully'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Unfollow a user."""
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.unfollow(user_to_unfollow)
        return Response({'detail': 'User unfollowed successfully'}, status=status.HTTP_200_OK)