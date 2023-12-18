from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('register/', user_views.RegisterUser.as_view(), name='register'),
    path('confirm_email/', TemplateView.as_view(template_name='shorterner/confirm_email.html'), name='confirm_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='shorterner/invalid_verify.html'), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>', user_views.EmailVerify.as_view(), name='verify_email'),
    path('profile/', user_views.profile_view, name='profile'),
    path('edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('edit_profile/password/',
         user_views.PasswordEditView.as_view(template_name='registration/change_password.html'), name='password_edit'),
    path('password_success/', user_views.password_success, name='password_success'),
    path('profile/urls', user_views.user_urls, name='user_urls'),
    
]
