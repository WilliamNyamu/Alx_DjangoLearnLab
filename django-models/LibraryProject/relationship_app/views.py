from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import request
from django.shortcuts import render, redirect
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
    return render(request,'librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')