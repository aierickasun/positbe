#import the model
from items.models import Items
#import the serializer
from items.serializers import ItemsSerializer

#import the rest_framework class/methods
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ItemsList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        items = Items.objects.all()
        serializers = ItemsSerializer(items,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ItemsDetail(APIView):
    def get_object(self, pk):
        try:
            return Items.objects.get(pk=pk)
        except Items.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemsSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
