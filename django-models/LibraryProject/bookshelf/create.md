from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
b
# Example output (yours may differ in PK):
# <Book: 1984 (1949)>