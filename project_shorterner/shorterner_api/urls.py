from django.urls import path
from . import views

urlpatterns = [
    path('short_url/', views.CreateShortUrl.as_view()),
    path('short_url/<str:short_url>', views.ShortUrlView.as_view()),
    path('email_verification/<uidb64>/<token>', views.EmailVerificationView.as_view(), name='verify_email_api')    
]
