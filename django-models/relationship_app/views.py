from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test



def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Correct template path
    context_object_name = 'library'


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('profile')  # Redirect to the profile page after registration
#     else:
#         form = UserCreationForm()
#     return render(request, 'relationship_app/register.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('profile')  # Redirect to the homepage or any other page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# # @login_required
# def profile_view(request):
#     return render(request, 'relationship_app/profile.html')
def profile_view(request):
    return render(request, 'profile.html')

# Use Django's built-in LoginView and LogoutView
class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = '/relationship/login/'  # Redirect to login after logout


















# Create your views here.
    # Check if the user has the Admin role
def is_admin(user):
    return user.userprofile.role == 'Admin'

# Check if the user has the Librarian role
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Check if the user has the Member role
def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')