from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Example output (tuple of rows deleted and a dict):
# (1, {'bookshelf.Book': 1})

list(Book.objects.all())
# Example output:
# []