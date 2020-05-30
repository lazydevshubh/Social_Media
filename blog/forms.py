from django import forms
from .models import Comment

class addComment(forms.ModelForm):
    content=forms.TextInput()

    class Meta:
        model=Comment
        fields=['content']

'''class UserUpdationForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model= User
        fields=['username','email']

class ProfileUpdationForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields=['image']
'''