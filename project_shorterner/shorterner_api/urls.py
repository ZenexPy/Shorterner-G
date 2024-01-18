from django.urls import path
from .views import ShorturlViewSet

urlpatterns = [
    path('all_urls/', ShorturlViewSet.as_view({'get': 'list'}), name='all_urls_api')
]