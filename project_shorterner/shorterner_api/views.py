from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortUrlSerializer
from rest_framework import generics
from shorterner.models import ShortURL


class ShortUrlView(APIView):
    

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
            return Response({'detail': 'Object not found'},status=status.HTTP_404_NOT_FOUND)
        response_data = {
            'status':'url was deleted',
            'deleted_object' : serializer.data
        }
        obj.delete()        
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    

class CreateShortUrl(APIView):


    def post(self, request, *args, **kwargs):
        serializer = ShortUrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)