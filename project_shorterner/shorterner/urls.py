from .views import *
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('shorterner.urls_user')),
    path('', shorterner_views.createShortUrl, name='index'),
    
]