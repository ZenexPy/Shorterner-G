from typing import Any
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from ..forms import RegisterUserForm, UserUpdateForm, AuthenticationFormCustom
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, authenticate, get_user_model, login
from ..models import ShortURL
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.contrib.sites.shortcuts import get_current_site
from ..tasks import send_email


User = get_user_model()


class RegisterUser(View):
    template_name = 'shorterner/register.html'

    def save_user_data(self, form, request):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        domain = get_current_site(request).domain
        send_email.delay(user.id, domain)
        return redirect('confirm_email')

    def get(self, request):
        context = {
            'form': RegisterUserForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_query = User.objects.filter(email=email)
            if user_query.exists():
                if user_query.filter(is_email_verified=True).exists():
                    context = {
                        'form': form,
                        'error_message': 'Этот e-mail уже зарегистрирован и верифицирован',
                    }
                    return render(request, self.template_name, context)
                else:
                    return self.save_user_data(form, request)
            else:
                return self.save_user_data(form, request)
        else:
            context = {
                'form': form
            }
            return render(request, self.template_name, context)


class LoginViewCustom(v.LoginView):
    form_class = AuthenticationFormCustom


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            login(request, user)
            return redirect('index')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class PasswordEditView(v.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


@login_required
def profile_view(request):
    return render(request, 'registration/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль успешно изменен')
            return HttpResponseRedirect(reverse_lazy('profile'))
    else:
        user_form = UserUpdateForm(instance=request.user)

        data = {
            'form': user_form
        }
        return render(request, 'registration/edit_profile.html', data)


def password_success(request):
    logout(request)
    return render(request, 'registration/password_success.html', {})


def user_urls(request):
    user = request.user
    urls = ShortURL.objects.filter(url_owner=user)
    return render(request, 'shorterner/my_urls.html', {'urls': urls})
