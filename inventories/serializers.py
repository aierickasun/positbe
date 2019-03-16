from rest_framework import serializers
from inventories.models import Inventories
from stores.serializers import StoresSerializer

class InventoriesSerializer(serializers.ModelSerializer):
    quantity = (serializers.IntegerField(min_value = 0))
    class Meta:
        model = Inventories
        fields = ('id', 'store', 'item', 'quantity', 'updated')
