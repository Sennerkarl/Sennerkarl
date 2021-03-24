from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Subscribed
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import PrependedText

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

    class Meta:
        model = Subscribed
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_show_labels = False
        self.helper.field_class = ''
        self.helper.layout = Layout(
            Field(PrependedText('content','Get Quarterly Reports', placeholder='Your Email'))
        )