from django.contrib import admin
from .models import Book
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
