from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email'] #overriding the default format and ensuring that the email is also displayed as a input field

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_photo']

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter a compelling title...',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 20,
                'placeholder': 'Write your blog post here ...',
                'data-editor': 'markdown'
            })
        }
        labels = {
            'title': 'Post Title',
            'Content': 'Post Content'
        }
        help_texts = {
            'title': 'This will be used to generate the URL slug',
        }

        def clean_title(self):
            """Validate title uniqueness and length"""
            title = self.cleaned_data['title']

            if len(title) < 10:
                raise forms.ValidationError(
                    "Title must be at least 10 characters long."
                )
            
            # Check for existing posts with the same title (excluding current instance if editing)
            existing = Post.objects.filter(title__iexact=title)
            if self.instance.pk:
                existing = existing.exclude(pk = self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError(
                    "A post with the title already exists."
                )
            return title
        
        def clean_content(self):
            """Ensure content meets the minimum length"""
            content = self.cleaned_date['content']

            if len(content) < 100:
                raise forms.ValidationError(
                    "Post content must be at least 100 characters long."
                )
            return content
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        