from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def custom_404(request, exception):
    return HttpResponseRedirect(reverse_lazy('index'))