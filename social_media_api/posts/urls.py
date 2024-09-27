# posts/urls.py

from django.urls import path, include
from .views import UserFeedView
from rest_framework.routers import DefaultRouter  # Add this line to import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Include the DRF router for posts and comments
    path('feed/', UserFeedView.as_view(), name='user_feed'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike_post'),

]