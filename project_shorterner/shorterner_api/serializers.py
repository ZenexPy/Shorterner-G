import re
from rest_framework import serializers
from shorterner.utils import save_short_url
from shorterner.models import ShortURL
from shorterner.utils import url_validation



class ShortUrlSerializer(serializers.ModelSerializer):

    short_url = serializers.CharField(required=False)

    class Meta:
        model =  ShortURL
        fields = ('original_url', 'short_url', 'redirect_count', 'expiration_date', 'created_at')
        

    def create(self, validated_data):
        original_url = validated_data.get('original_url')
        r = re.compile(url_validation)
        if (re.search(r, original_url)):
            s = save_short_url(original_url)

            validated_data['short_url'] = s.short_url
            validated_data['redirect_count'] = 0
            validated_data['expiration_date'] = s.expiration_date
            validated_data['created_at'] = s.created_at

            return ShortURL.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("Invalid URL")
    



