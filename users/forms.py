from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, CURRENCY_CHOICES, TIMEZONE_CHOICES


class EmailOrUsernameAuthForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def clean(self):
        identifier = self.cleaned_data.get('username')
        password   = self.cleaned_data.get('password')
        if identifier and password:
            # try email lookup first
            if '@' in identifier:
                try:
                    user_obj = User.objects.get(email=identifier)
                    identifier = user_obj.username
                except User.DoesNotExist:
                    pass
            self.user_cache = authenticate(self.request, username=identifier, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid username/email or password.')
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'preferred_currency', 'timezone', 'country')
        widgets = {
            'first_name':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email':              forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'preferred_currency': forms.Select(attrs={'class': 'form-select'}),
            'timezone':           forms.Select(attrs={'class': 'form-select'}),
            'country':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Nigeria, Kenya, USA'}),
        }
