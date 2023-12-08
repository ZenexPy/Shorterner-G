from django.db import models

class ShortURL(models.Model):
    original_url=models.CharField(max_length=700)
    short_url=models.CharField(max_length=100)
    created_at=models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.original_url