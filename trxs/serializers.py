from rest_framework import serializers
from trxs.models import Trxs, TrxsReceipt

class TrxsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trxs
        fields = ('id','sale_total','store','sale_time')

class TrxsReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrxsReceipt
        fields = ('quantity','items','trxs')
