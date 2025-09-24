from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Book, Librarian
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
# Create your views here.

def index(request):
    return render(request, "relationship_app/index.html")


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


# --- Helper functions ---
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Member"

# --- Views ---
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# Add book view
@permission_required('relationship_app.can_add_book')
def add_book(request):
    # logic to add book
    return render(request, 'relationship_app/add_book.html')


# Edit book view
@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # logic to edit book
    return render(request, 'relationship_app/edit_book.html', {'book': book})


# Delete book view
@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # logic to delete book
    return redirect('list_books')