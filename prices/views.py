#import the model
from prices.models import Prices
#import the serializer
from prices.serializers import PricesSerializer

#import the rest_framework class/methods
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

class PricesDetail(APIView):
    def get_object(self, pk):
        try:
            return Prices.objects.get(pk=pk)
        except Prices.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        price = self.get_object(pk)
        serializer = PricesSerializer(price)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        price = self.get_object(pk)
        serializer = PricesSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        price = self.get_object(pk)
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
