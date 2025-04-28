from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("password don't match!")
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href='../password/'>this form</a>.")

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login', "is_superuser"]


class UserRegisterationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Enter your email',
            'style': 'max-width: 300px;',
        }),
        label="Email"
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Enter your full name',
            'style': 'max-width: 300px;',
        }),
        label="Full Name"
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Enter your phone number',
            'style': 'max-width: 300px;',
        }),
        label="Phone Number"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Enter your password',
            'style': 'max-width: 300px;',
        }),
        label="Password"
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        print(f"this is email: {email}")
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email has already been taken")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("This phone number has already been taken")
        return phone

class VarifyCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',  # Added 'form-control-sm' for smaller width
            'placeholder': 'Enter your phone number',
            'style': 'max-width: 300px;',  # Inline style to limit the width
        }),
        label="Phone Number"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',  # Added 'form-control-sm' for smaller width
            'placeholder': 'Enter your password',
            'style': 'max-width: 300px;',  # Inline style to limit the width
        }),
        label="Password"
    )