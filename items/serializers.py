from rest_framework import serializers
from items.models import Items


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ('id','item_name','price','vendor','updated')
