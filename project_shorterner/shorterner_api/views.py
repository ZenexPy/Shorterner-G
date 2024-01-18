from shorterner.models import ShortURL
from rest_framework import viewsets
from .serializers import ShorturlSerializer


class ShorturlViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShorturlSerializer