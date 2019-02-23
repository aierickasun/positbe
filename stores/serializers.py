from rest_framework import serializers
from stores.models import Stores


class StoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = ('id','store_name','store_address','store_city','store_state')
