from rest_framework import serializers
from inventories.models import Inventories
from stores.serializers import StoresSerializer

class InventoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventories
        fields = ('id', 'store', 'item', 'quantity', 'updated')