from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import the views from your app
from .views import register
from .views import profile_view
# urlpatterns = [
#     path('books/', list_books, name='list_books'),  # Function-based view
#     path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
#  path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
#     path('register/', register, name='register'),

# ]
urlpatterns = [
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),  # Assuming you have a profile view
]

