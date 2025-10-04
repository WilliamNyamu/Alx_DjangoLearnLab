from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, UserInfoForm, ProfileInfoForm
from django.contrib.auth.decorators import login_required

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


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserInfoForm(request.POST, instance=request.user)
        p_form = ProfileInfoForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserInfoForm(instance=request.user)
        p_form = ProfileInfoForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'blog/profile.html', context)

            

