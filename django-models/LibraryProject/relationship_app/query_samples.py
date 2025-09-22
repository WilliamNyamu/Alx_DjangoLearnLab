from .models import Author, Book

def queries():
    # Query all books by a specific author
    author = Book.objects.get(author = "Prof Kibugi")
    books_by_author = Book.objects.filter(author = author)
