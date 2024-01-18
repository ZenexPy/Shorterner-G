from django.urls import path
from .views import ShorturlApi

urlpatterns = [
    path('shorterner/', ShorturlApi.as_view(), name='all_urls_api')
]