from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, UserInfoForm, ProfileInfoForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
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
        # instance is required to populate the profile of the currently authenticated user
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
    template_name = "blog/post_list.html"
    context_object_name = 'posts'

class PostDetailView(generic.DetailView):
    queryset = Post.objects.all()
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreateForm
    template_name = 'blog/post_form.html'
    login_url = '/login/'
    success_url = reverse_lazy('posts')
    

    def form_valid(self, form):
        """Ensure the author is the currently authenticated user"""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Render a message when form has errors """
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        """
        This method is needed by the UserPassesTestMixin
        Allow only the author to edit their own post
        """
        post = self.get_object() # Retrieves the current post being edited
        return self.request.user == post.author 
    
    # If the currently authenticated user is the author, it returns True, if not, false
    # By default, if false, django will populate a 403 Forbidden error, unless overridden by handle_no_permission method

    def handle_no_permission(self):
        """Custom message when no permission(if test_func returns false)"""
        messages.error(self.request, "You can only edit your own articles")
        return redirect('posts')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('posts')
    context_object_name = 'post'

    def test_func(self):
        """Only author or is_staff can delete the post"""
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "Only the author or an admin staff can delete this post")
        return redirect('posts')
    