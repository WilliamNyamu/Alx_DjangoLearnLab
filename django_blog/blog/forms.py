from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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
