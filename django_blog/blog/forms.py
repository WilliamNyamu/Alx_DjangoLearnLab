from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag

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
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': "Post a comment ..."
            })
        }

class TagForm(forms.ModelForm):
    # A simple textarea or text input where users enter tags separated by commas
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, python, tutorial)",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        # add other fields if needed (image, etc.)

    def __init__(self, *args, **kwargs):
        # If instance provided (update view), prefill tags field from instance tags
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tags'].initial = ', '.join([t.name for t in instance.tags.all()])

    def save(self, commit=True):
        # Save the Post object first, then handle tags
        post = super().save(commit=commit)
        tag_string = self.cleaned_data.get('tags', '')
        # parse tag string: split by comma, strip whitespace, ignore empties
        tag_names = [t.strip() for t in tag_string.split(',') if t.strip()]
        # Get or create Tag objects, then set m2m
        tags = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            # Note: using get_or_create with case-insensitive check requires custom handling:
            # above we try name__iexact in get_or_create to avoid case duplicates. If DB backend
            # does not allow name__iexact in get_or_create, fallback to:
            # tag_obj, created = Tag.objects.get_or_create(name=name)
            tags.append(tag_obj)
        # Assign tags to the post
        post.tags.set(tags)
        # If commit=False was used, tags assignment will still work after the instance is saved.
        return post