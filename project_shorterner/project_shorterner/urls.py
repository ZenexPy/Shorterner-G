from django.urls import path, include
from shorterner.views import *

urlpatterns = [
    path('shorterner/', include('shorterner.urls')),
    path('', include('django.contrib.auth.urls')),
    path('<str:url>', redirect, name='redirect'),
    ]