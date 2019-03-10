from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#import the model
from trxs.serializers import TrxsSerializer, TrxsReceiptReadSerializer, TrxsReceiptPostSerializer
#import the serializer
from trxs.models import Trxs, TrxsReceipt

class TrxsList(APIView):
    def get(self, request, format=None):
        trxs = Trxs.objects.all()
        serializers = TrxsSerializer(trxs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = TrxsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TrxsDetail(APIView):
    def get_object(self, pk):
        try:
            return Trxs.objects.get(pk=pk)
        except Trxs.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        trx = self.get_object(pk)
        serializer = TrxsSerializer(trx)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        trx = self.get_object(pk)
        serializer = TrxsSerializer(trx, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        trx = self.get_object(pk)
        trx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrxsReceiptDetail(APIView):
    def get_object(self, pk):
        try:
            return TrxsReceipt.objects.filter(id=pk)
        except TrxsReceipt.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # this pulls the models object from the database creating a Python object
        trxreceipt = TrxsReceipt.objects.filter(trxs_id=pk)
        # this deserializes the object
        serializer = TrxsReceiptReadSerializer(trxreceipt,many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        # this deserializes the object coming in post-type where the primary keys are only needed.
        serializer = TrxsReceiptPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        trx_receipt_id = request.query_params.get('transactionReceiptId', None)
        if trx_receipt_id is None:
            return Response({"message":"transactionReceiptId query param not found"}, status=status.HTTP_400_BAD_REQUEST)
        trx_receipt_obj = self.get_object(trx_receipt_id)
        if trx_receipt_obj:
            trx_receipt_obj.delete()
        else:
            return Response({"message":"transaction_id not found"}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
