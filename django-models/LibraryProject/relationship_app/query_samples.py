from .models import Author, Book, Library

def queries():
    # Query all books by a specific author
    author_name = "Prof Kibugi"
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)

    # List all the books in a library
    library_name = "LibraryProject"
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    
