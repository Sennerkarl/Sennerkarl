from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Subscribed

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta: #nested namespace for configurations
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta: #nested namespace for configurations
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
            attrs={
                'placeholder': 'Your email goes here',
                'class': "form-control",
                #'style': 'width: 200px; height:40px; border-style:none; border-radius:5px; margin-right:-10px; padding-left:5px'
            }))
    class Meta:
        model = Subscribed
        fields = ['email']
