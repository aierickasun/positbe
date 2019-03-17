from rest_framework import serializers
from items.models import Items
from vendors.serializers import VendorsSerializer


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ('id','item_name','price','vendor','updated')

class ItemsReadSerializer(serializers.ModelSerializer):
    vendor = VendorsSerializer()
    class Meta:
        model = Items
        fields = ('id','item_name','price','vendor','updated')
