from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, UserInfoForm, ProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Post

# Create your views here.

def index(request):
    return render(request, 'blog/home.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'blog/logout.html')


@login_required # Ensure only logged in user is accessing this view
def profile(request):
    if request.method == "POST":
        # Bind the submitted POST data (and files) to the forms
        # UserInfoForm edits the built-in User model
        u_form = UserInfoForm(request.POST, instance=request.user)

        # ProfileInFoForm edits the custom Profile model
        # request.FILES is needed to handle image/file uploads
        p_form = ProfileInfoForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        # If it's a GET request, pre-fill forms with the current user data
        u_form = UserInfoForm(instance=request.user)
        p_form = ProfileInfoForm(instance=request.user.profile)
    
    # Pass both forms into the template for rendering
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'blog/profile.html', context)


# View for displaying all blog posts
class PostsView(generic.ListView):
    queryset = Post.objects.all() # You put the queryset not the model
    template_name = "blog/blog.html"
    context_object_name = 'posts'

