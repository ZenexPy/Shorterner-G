import re
from rest_framework import serializers
from shorterner.utils import save_short_url
from shorterner.models import ShortURL
from shorterner.utils import url_validation
from django.contrib.auth import get_user_model
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers
from shorterner.tasks import send_email
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()


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
        



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )
        return user
    


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        
        validated_data = super().validate(attrs)

        user = self.user
        if user.is_email_verified:
            return validated_data
        else:
            request = self.context.get('request')
            domain = get_current_site(request).domain
            send_email.delay(user.id, domain)
            raise serializers.ValidationError("Email is not verified. Check your email for verification letter")
