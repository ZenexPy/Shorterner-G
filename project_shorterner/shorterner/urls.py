from .views import *
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redirect/<int:obj_id>/', shorterner_views.redirect_page, name='redirect_page'),
    path('users/', include('shorterner.urls_user')),
    path('page_not_found/', TemplateView.as_view(template_name='shorterner/pagenotfound.html'), name='page_not_found'),
    path('', shorterner_views.createShortUrl, name='index'),
]