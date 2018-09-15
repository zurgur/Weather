from django.contrib.auth.models import User
from .models import Profile
from django import forms

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username','password','email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location']

class LoginnForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']