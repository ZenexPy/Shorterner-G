import random
import string
import re


from django.shortcuts import render
from django.urls import reverse_lazy
from ..models import ShortURL
from django.http import HttpResponseRedirect
from ..forms import FormAddUrl
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


url_validation = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
random_chars_list = list(string.ascii_letters+string.digits)


def makeRandomList():
    string_chars = "".join(random.choices(random_chars_list, k=7))
    return string_chars


def makeUniqueUrl():
    list_random = makeRandomList()

    while len(ShortURL.objects.filter(short_url=list_random)) != 0:
        list_random = makeRandomList()
    return list_random


def redirect(request, url):
    try:
        current_obj = ShortURL.objects.get(short_url=url)
    except ObjectDoesNotExist:
        return render(request, 'shorterner/pagenotfound.html')
    original_url = current_obj.original_url
    return HttpResponseRedirect(original_url)


def createShortUrl(request):
    if request.method == 'POST':
        form = FormAddUrl(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']

            r = re.compile(url_validation)
            if (re.search(r, original_website)):
                d = datetime.now()
                s = ShortURL(original_url=original_website,
                             short_url=makeUniqueUrl(), created_at=d)
                s.save()
                return render(request, 'shorterner/redirect.html', {'obj': s})
            else:
                messages.error(request, f'Вы ввели неправильный URL')
                return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = FormAddUrl()
        context = {'form': form}
        return render(request, 'shorterner/index.html', context)
