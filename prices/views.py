from prices.models import Prices
from prices.serializers import PricesSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class PricesList(APIView):
    def get(self, request, format=None):
        prices = Prices.objects.all()
        serializers = PricesSerializer(prices,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = PricesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
