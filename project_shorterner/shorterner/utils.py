import random
import string
import re

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import ShortURL
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib import messages
from typing import List

random_chars_list = list(string.ascii_letters+string.digits)
url_validation = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"


def make_letters() -> List:
    string_chars = "".join(random.choices(random_chars_list, k=7))
    return string_chars


def make_unique_url() -> str:
    random_short_url = make_letters()

    while len(ShortURL.objects.filter(short_url=random_short_url)) != 0:
        random_short_url = make_letters()
    return random_short_url


def date_calculate():
    d = datetime.now()
    expiration_date = timezone.now() + relativedelta(months=1)
    return d, expiration_date

created_at, expiration_date = date_calculate()

def save_short_url(original_url: str):
    
    s = ShortURL(original_url=original_url, short_url=make_unique_url(), created_at=created_at,  expiration_date=expiration_date)
    return s
    

def is_user_authenticated(request, new_url):
    if request.user.is_authenticated:
        new_url.url_owner = request.user
        return new_url