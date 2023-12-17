from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShortURL, User

admin.site.register(ShortURL)
admin.site.register(User, UserAdmin)
