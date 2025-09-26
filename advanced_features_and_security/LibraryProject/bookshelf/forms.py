from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")