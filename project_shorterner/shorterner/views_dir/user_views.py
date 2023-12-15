from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from ..forms import RegisterUserForm, UserUpdateForm
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as v
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shorterner/register.html'
    success_url = reverse_lazy('login')


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


class PasswordEditView(v.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
