from rest_framework import serializers
from prices.models import Prices


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id','item_name','price','vendor','updated')
