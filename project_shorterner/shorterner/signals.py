from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=User)
def handle_email_verification(sender, instance, created, **kwargs):
    if not created and instance.is_email_verified:
        other_users = User.objects.filter(email=instance.email, is_email_verified=False).exclude(username=instance.username)
        other_users.delete()