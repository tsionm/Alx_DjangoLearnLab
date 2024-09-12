from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagField


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class PostForm(forms.ModelForm):
    tags = TagField(required=False)  # Updated to use TagField

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class PostForm(forms.ModelForm):
#     tags = TagField(required=False) 

#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'tags']


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']

# # class PostForm(forms.ModelForm):
# #     tags = forms.CharField(widget=TagWidget(), required=False)

# #     class Meta:
# #         model = Post
# #         fields = ['title', 'content', 'tags']  # Include tags in fields
