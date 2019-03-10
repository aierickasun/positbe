from rest_framework import serializers
from trxs.models import Trxs, TrxsReceipt

class TrxsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trxs
        fields = ('id','sale_total','store','sale_time')

class TrxsReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrxsReceipt
        fields = ('id','quantity','items','trxs')
        extra_kwargs = {'trxs' : {'write_only':True}}

# class TrxsIndSerializer(serializers.ModelSerializer):
#     transaction_ind = serializers.StringRelatedField(read_only = True)
#     class Meta:
#         model = Trxs
#         fields = ""
#         # fields = ('id','sale_total','store','sale_time','transaction_ind')
#         # extra_kwargs = {'trxs' : {'write_only':True}}
