from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from trxs.serializer import TrxsSerializer
from trxs.models import Trxs

class TrxstList(APIView):
    def get(self,request,format=None):
        transactions = Trxs.objects.all()
        serializer = TrxsSerializer(transactions,many=True)
        return Reponse(serializer.data)

# Create your views here.
