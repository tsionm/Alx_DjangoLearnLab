# # api/urls.py

# from django.urls import path
# from .views import BookList

# urlpatterns = [
#     path('books/', BookList.as_view(), name='book-list'),
# ]
# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
    # path('booklist/', BookList.as_view(), name='book-list'),  # Adjust the path as needed
]