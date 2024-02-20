from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, SetPasswordForm, PasswordResetForm
from .models import User,Profile

# class RegistrationForm(forms.Form):
#     username = forms.CharField(max_length=200)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=100, required=True, help_text='Enter your full name.')

    class Meta:
        model =User
        fields = ['username', 'full_name','email', 'password1', 'password2']
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise forms.ValidationError('Username must be at least 5 characters long.')
        if User.objects.filter(username=username).exists():
             raise forms.ValidationError('Username cannot be an existing username.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if len(full_name) < 8:
            raise forms.ValidationError('Full name must be at least 8 characters long.')
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Invalid email address.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email cannot be an existing email.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


class UserLoginForm(AuthenticationForm,BaseException):
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        return password
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise forms.ValidationError('Username must be at least 5 characters long.')

        return username
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','image']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model =User
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

