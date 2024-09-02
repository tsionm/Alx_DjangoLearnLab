from django.db import models

# Author model represents an author in the system.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Ensure this line is indented correctly

# Book model represents a book, with a foreign key relationship to Author.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title  # Ensure this line is indented correctly

# Create your models here.
