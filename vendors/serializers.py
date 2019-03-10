from rest_framework import serializers
from vendors.models import Vendors

class VendorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ('id','vendor_name','vendor_address','vendor_city','vendor_name')
