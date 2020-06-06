from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile,Message

class messageForm(forms.ModelForm):
    message=forms.CharField(max_length=1000)

    class Meta:
        model=Message
        fields=['message']

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserUpdationForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model= User
        fields=['username','email']

class ProfileUpdationForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields=['image']