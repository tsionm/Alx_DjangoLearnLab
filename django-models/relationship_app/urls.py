from django.urls import path
from .views import list_books, LibraryDetailView
from .views import register
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import the views from your app

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
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),  # Profile view
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_book/', views.add_book_view, name='add_book'),  # URL for adding a book
    path('edit_book/<int:pk>/', views.edit_book_view, name='edit_book'),  # URL for editing a book
    # Add other URL patterns as needed
    # Other URL patterns...python manage.py makemigrations


]

