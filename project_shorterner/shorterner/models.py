from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta



class ShortURL(models.Model):
    original_url = models.CharField(max_length=700)
    short_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    url_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    def __str__(self) -> str:
        return self.original_url
    

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email