from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class ShortURL(models.Model):
    original_url = models.CharField(max_length=700)
    short_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    url_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.original_url
    
# @receiver(pre_save, sender=ShortURL)
# def set_user_to_url(sender, instance, *args, **kwargs): #sender - модель, которая отправляет, instance - экземляр модели, модели, которая вызвала, create - была ли добавлена новая запись в бд(true, false)
#     if
#         if not instance.pk:
#         instance.url_owner = instance.url_owner