from django.http import Http404
#import the rest_framework class/methods
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


#import the model
from vendors.models import Vendors
#import the serializer
from vendors.serializers import VendorsSerializer


class VendorsList(APIView):
    def get(self, request, format=None):
        vendors = Vendors.objects.all()
        serializers = VendorsSerializer(vendors,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = VendorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VendorsDetail(APIView):
    def get_object(self, pk):
        try:
            return Vendors.objects.get(pk=pk)
        except Vendors.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorsSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorsSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
