#import the rest_framework class/methods
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#import the model
from stores.models import Stores
#import the serializer
from stores.serializers import StoresSerializer


class StoresList(APIView):
    def get(self, request, format=None):
        stores = Stores.objects.all()
        serializers = StoresSerializer(stores,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = StoresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StoresDetail(APIView):
    def get_object(self, pk):
        try:
            return Stores.objects.get(pk=pk)
        except Stores.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        store = self.get_object(pk)
        serializer = StoresSerializer(store)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        store = self.get_object(pk)
        serializer = StoresSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        store = self.get_object(pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
