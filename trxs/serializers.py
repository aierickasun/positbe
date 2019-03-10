from rest_framework import serializers
from items.serializers import ItemsSerializer
from trxs.models import Trxs, TrxsReceipt

class TrxsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trxs
        fields = ('id','sale_total','store','sale_time')

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
