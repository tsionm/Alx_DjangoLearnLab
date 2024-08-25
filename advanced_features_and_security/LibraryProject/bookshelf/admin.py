from django.contrib import admin
from .models import Book
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ['username', 'email', 'date_of_birth', 'profile_photo']

admin.site.register(CustomUser, CustomUserAdmin)

# Custom BookAdmin to manage how the Book model is displayed in the admin
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality for title and author
    search_fields = ('title', 'author')
    
    # Add filter options by publication year
    list_filter = ('publication_year',)

admin.site.register(Book)
# Register your models here.
