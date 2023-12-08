from .views import *
from django.urls import path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('', createShortUrl, name='index'),
]