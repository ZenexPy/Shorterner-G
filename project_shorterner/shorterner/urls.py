from .views import *
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_profile/password/', 
         auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('', createShortUrl, name='index'),
    
]