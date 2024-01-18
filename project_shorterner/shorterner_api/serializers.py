from rest_framework import serializers

from shorterner.models import ShortURL

class ShorturlSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ShortURL
        fields = ('original_url', 'short_url', 'expiration_date')