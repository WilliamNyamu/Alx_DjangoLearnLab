from .models import Author, Book, Library

def queries():
    # Query all books by a specific author
    author = Book.objects.get(author = "Prof Kibugi")
    books_by_author = Book.objects.filter(author = author)

    # List all the books in a library
    lib_name = Library.objects.get(name = "LibraryProject")
    for book in lib_name.books.all():
        print(book)
