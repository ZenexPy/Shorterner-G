from project_shorterner.celery import app
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import ShortURL
from project_shorterner.celery import app
from dateutil.relativedelta import relativedelta


@shared_task
def send_email(user_id, domain):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    message = render_to_string('shorterner/verify_email.html', context)
    email = EmailMessage(
        'Verify your email',
        message,
        to=[user.email]
    )
    email.send()

@shared_task
def delete_expired_links():
    expired_date = timezone.now()-relativedelta(month=1)

    expired_links = ShortURL.objects.filter(created_at__lte=expired_date) #поменять на exp date

    expired_links.delete()

app.conf.beat_schedule = {
    'task_exprired_links': {
        'task': 'shorterner.tasks.delete_expired_links',
        'schedule': 10800,
    },
}



# def send_email_for_verify(request, user):
#     current_site = get_current_site(request)
#     context = {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': token_generator.make_token(user),
#     }
#     message = render_to_string(
#         'shorterner/verify_email.html',
#         context=context,
#     )
#     email = EmailMessage(
#         'Veryfi email',
#         message,
#         to=[user.email],
#     )
#     email.send()