from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from relationship_app.models import Book

# Create your views here.
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            
            cleaned_data = form.cleaned_data
            return render(request, "bookshelf/form_success.html", {"data": cleaned_data})
    else:
        form = ExampleForm()

    return render(request, "bookshelf/example_form.html", {"form": form})