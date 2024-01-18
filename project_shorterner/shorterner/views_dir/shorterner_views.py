import random
import string
import re


from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from ..models import ShortURL
from django.http import HttpResponseRedirect
from ..forms import FormAddUrl
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from ..utils import *





def redirect(request, url):
    try:
        current_obj = ShortURL.objects.get(short_url=url)
    except ObjectDoesNotExist:
        return render(request, 'shorterner/pagenotfound.html')
    current_obj.redirect_count += 1
    current_obj.save()
    original_url = current_obj.original_url
    return HttpResponseRedirect(original_url)


def index(request):
    if request.method == 'POST':
        form = FormAddUrl(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            r = re.compile(url_validation)
            if (re.search(r, original_website)):
                object_url = makeShortUrl(request, original_website)
                obj_id = object_url.pk
                redirect_url = reverse_lazy('redirect_page', args=(obj_id, ))
                return HttpResponseRedirect(redirect_url)
            else:
                messages.error(request, f'Вы ввели неправильный URL')
                return HttpResponseRedirect(reverse_lazy('index'))
            
            
                
    else:
        form = FormAddUrl()
        context = {'form': form}
        return render(request, 'shorterner/index.html', context)


def redirect_page(request, obj_id):
    obj = get_object_or_404(ShortURL, pk=obj_id)
    return render(request, 'shorterner/redirect.html', {'obj': obj})