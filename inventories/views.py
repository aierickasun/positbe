from django.http import Http404
from inventories.models import Inventories
from inventories.serializers import InventoriesSerializer, InventoriesReadSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class InventoriesList(APIView):
    def get(self, request, format=None):
        inventories = Inventories.objects.all()
        serializers = InventoriesReadSerializer(inventories,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = InventoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InventoriesDetail(APIView):
    def get_object(self, pk):
        try:
            return Inventories.objects.get(pk=pk)
        except Inventories.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        inventory = self.get_object(pk)
        serializer = InventoriesSerializer(inventory)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        inventory = self.get_object(pk)
        serializer = InventoriesSerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inventory = self.get_object(pk)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
