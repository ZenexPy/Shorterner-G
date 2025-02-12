from django.urls import path, include
from django.contrib.auth import views as auth_views
from shorterner.views import *
from shorterner_api.views import UserRegistrationViewCustom

#from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)


urlpatterns = [
    path('shorterner/', include('shorterner.urls')),
    path('api/', include('shorterner_api.urls')),
    path('api/auth/users/', UserRegistrationViewCustom.as_view(), name='user-registration'),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('login/', user_views.LoginViewCustom.as_view(), name='login'),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html'), name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_done.html'),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_confirm.html'),name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/password_complete.html'),name="password_reset_complete"),
    path('', include('django.contrib.auth.urls')),
    path('<str:url>', shorterner_views.redirect),
    ]

handler404 = 'shorterner.handlers.custom_404'