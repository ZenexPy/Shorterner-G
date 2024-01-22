from django.urls import path
from . import views

urlpatterns = [
    path('short_url/', views.CreateShortUrl.as_view()),
    path('short_url/<str:short_url>', views.ShortUrlView.as_view()),    
]