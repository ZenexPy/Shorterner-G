from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', user_views.RegisterUser.as_view(), name='register'),
    path('profile/', user_views.profile_view, name='profile'),
    path('edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('edit_profile/password/',
         user_views.PasswordEditView.as_view(template_name='registration/change_password.html'), name='password_edit'),
    path('password_success/', user_views.password_success, name='password_success'),
    
]
