from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateShortUrlSerializer, UrlDetailSerializer
from rest_framework import generics
from shorterner.models import ShortURL


class CreateShortUrlView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = CreateShortUrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

class GetInfoUrlView(generics.RetrieveAPIView):

    queryset = ShortURL.objects.all()
    serializer_class = UrlDetailSerializer
    lookup_field = 'short_url'