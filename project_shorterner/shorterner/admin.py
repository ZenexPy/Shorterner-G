from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShortURL, User

class CustomUserAdmin(UserAdmin):
    list_display=('username', 'email', 'is_staff', 'is_email_verified')

admin.site.register(ShortURL)
admin.site.register(User, CustomUserAdmin)
