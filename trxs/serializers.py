from rest_framework import serializers
from items.serializers import ItemsSerializer
from trxs.models import Trxs, TrxsReceipt

class TrxsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trxs
        fields = ('id','tax_dollars','sale_dollars','sale_total','store','sale_time')

class TrxsReceiptReadSerializer(serializers.ModelSerializer):

    items = ItemsSerializer()
    class Meta:
        model = TrxsReceipt
        fields = ('id','items','quantity','trxs')
        # read_only_fields = ('items',)
    # def create(self,validated_data):
    #     print (validated_data)
    #     return

class TrxsReceiptPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrxsReceipt
        fields = ('id','items','quantity','trxs')

class CartItemsSerializer(serializers.Serializer):
    items_id = serializers.CharField()
    quantity = serializers.IntegerField()

class TrxsEnginePostSerializer(serializers.Serializer):
    # sub_cart_items = CartItemsSerializer()
    store = serializers.IntegerField()
    #do not allow an empty cart
    cart_items = CartItemsSerializer(many=True,allow_empty=False)
