from django.urls import path
from . import views

urlpatterns = [
    path('make_url/', views.CreateShortUrlView.as_view()),
    path('get_info/<str:short_url>', views.GetInfoUrlView.as_view())
]