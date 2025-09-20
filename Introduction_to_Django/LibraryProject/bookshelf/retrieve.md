from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
# Example output:
# (1, '1984', 'George Orwell', 1949)