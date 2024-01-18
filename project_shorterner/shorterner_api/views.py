from shorterner.models import ShortURL
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShorturlSerializer
from shorterner.views import *


class ShorturlApi(APIView):
    
    def post(self, request, *args, **kwargs):
        original_url = request.data.get('')
        serializer = ShorturlSerializer(data=request.data)
        serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)