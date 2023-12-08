from django import forms
from .models import ShortURL
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-input'}),
            'password2': forms.PasswordInput(attrs={'class':'form-input'})
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email')
