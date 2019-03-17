from rest_framework import serializers
from inventories.models import Inventories
from stores.serializers import StoresSerializer
from items.serializers import ItemsSerializer

class InventoriesSerializer(serializers.ModelSerializer):
    quantity = (serializers.IntegerField(min_value = 0))
    class Meta:
        model = Inventories
        fields = ('id', 'store', 'item', 'quantity', 'updated')

class InventoriesReadSerializer(serializers.ModelSerializer):
    item = ItemsSerializer()
    store = StoresSerializer()
    class Meta:
        model = Inventories
        fields = ('id','store','item','quantity','updated')
