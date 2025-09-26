from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from relationship_app.models import Book

# Create your views here.
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
