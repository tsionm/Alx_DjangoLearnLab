# posts/urls.py

from django.urls import path, include
from .views import UserFeedView
from rest_framework.routers import DefaultRouter  # Add this line to import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Include the DRF router for posts and comments
    path('feed/', UserFeedView.as_view(), name='user_feed'),
]