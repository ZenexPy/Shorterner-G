from django.db import models
from django.contrib.auth.models import User, AbstractUser



class ShortURL(models.Model):
    original_url = models.CharField(max_length=700)
    short_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    url_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.original_url
    

class User(AbstractUser):
    pass