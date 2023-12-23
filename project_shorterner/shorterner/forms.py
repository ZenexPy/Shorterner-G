from django import forms
from .models import ShortURL
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from .utils import send_email_for_verify
from django.core.exceptions import ValidationError

class FormAddUrl(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url']
        widgets ={
            'original_url': forms.TextInput(attrs={'class':'form-control'})
        }
        labels = {'original_url':'Поле для ввода Вашего Url'}

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()


    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-input'}),
            'password2': forms.PasswordInput(attrs={'class':'form-input'})
        }


class AuthenticationFormCustom(AuthenticationForm):


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

            if not self.user_cache.is_email_verified:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Ваш e-mail не верифицирован, пожалуйста проверьте свою почту!',
                    code='invalid_login',
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
