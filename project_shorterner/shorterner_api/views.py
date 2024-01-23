from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortUrlSerializer, UserSerializer
from rest_framework import generics
from shorterner.models import ShortURL
from rest_framework import permissions, exceptions
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as \
    token_generator


User = get_user_model()

class ShortUrlView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()



    def get(self, request, short_url):

        if short_url is not None:
            try:
                obj = ShortURL.objects.get(short_url=short_url)
                serializer = ShortUrlSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ShortURL.DoesNotExist:
                return Response({'detail': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'short_url parametr is missing'}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, short_url):


        try:
            obj = ShortURL.objects.get(short_url=short_url)
            serializer = ShortUrlSerializer(obj)
        except ShortURL.DoesNotExist:
            return Response({'detail': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        if obj.url_owner != request.user:
            raise exceptions.PermissionDenied("You should be owner of URL to delete one!")
        response_data = {
            'status':'url was deleted',
            'deleted_object' : serializer.data
        }
        
        obj.delete()        
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    

class CreateShortUrl(APIView):
    
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ShortUrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            url_owner = request.user if request.user.is_authenticated else None
            serializer.save(url_owner=url_owner)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

class UserRegistrationViewCustom(generics.CreateAPIView):

    serializer_class = UserSerializer
    

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_verification_email(user)
        

    def send_verification_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('shorterner_api/verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
        

class EmailVerificationView(generics.GenericAPIView):
                
        
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
        
