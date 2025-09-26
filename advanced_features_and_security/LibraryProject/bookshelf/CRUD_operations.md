Create

Create.md

from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
b
# Example output (yours may differ in PK):
# <Book: 1984 (1949)>

Retrieve

Retrieve.md

from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
# Example output:
# (1, '1984', 'George Orwell', 1949)

Update

Update.md

from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
# Example output:
# 'Nineteen Eighty-Four'


#Delete

#Delete.md

from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Example output (tuple of rows deleted and a dict):
# (1, {'bookshelf.Book': 1})

list(Book.objects.all())
# Example output:
# []



Filters + ordering 

from bookshelf.models import Book
Book.objects.create(title="Django for APIs", author="William S. Vincent", publication_year=2020)
Book.objects.create(title="Two Scoops of Django", author="Greenfeld & Roy", publication_year=2023)
Book.objects.create(title="Clean Code", author="Robert C. Martin", publication_year=2008)

# Filter by category-equivalent (we only have year/author/title in spec):
Book.objects.filter(author__icontains="django")

# Order by year ascending / descending:
Book.objects.all().order_by("publication_year")
Book.objects.all().order_by("-publication_year")