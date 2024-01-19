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

random_chars_list = list(string.ascii_letters+string.digits)
url_validation = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"


def makeRandomList():
    string_chars = "".join(random.choices(random_chars_list, k=7))
    return string_chars


def makeUniqueUrl():
    random_short_url = makeRandomList()

    while len(ShortURL.objects.filter(short_url=random_short_url)) != 0:
        random_short_url = makeRandomList()
    return random_short_url


def date_calculate():
    d = datetime.now()
    expiration_date = timezone.now() + relativedelta(months=1)
    return d, expiration_date

created_at, expiration_date = date_calculate()

def makeShortUrl(request, original_url):
    
    s = ShortURL(original_url=original_url, short_url=makeUniqueUrl(), created_at=created_at,  expiration_date=expiration_date)
    if request.user.is_authenticated:
        s.url_owner = request.user
        s.save()
        return s
    

def makeShortUrlApi(original_url):

    s = ShortURL(original_url=original_url, short_url=makeUniqueUrl(), created_at=created_at,  expiration_date=expiration_date)
    return s    