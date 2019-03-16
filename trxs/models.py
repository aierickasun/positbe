from django.db import models
from stores.models import Stores
from items.models import Items

class Trxs(models.Model):
    tax_dollars = models.DecimalField(decimal_places=2,max_digits=12,default=00.00)
    sale_dollars = models.DecimalField(decimal_places=2,max_digits=12,default=00.00)
    sale_total = models.DecimalField(decimal_places=2,max_digits=12,default=00.00)    
    store = models.ForeignKey('stores.Stores',on_delete=models.CASCADE)
    sale_time = models.DateTimeField(auto_now_add=True)


class TrxsReceipt(models.Model):
    quantity = models.PositiveIntegerField()
    items = models.ForeignKey('items.Items',on_delete=models.CASCADE)
    trxs = models.ForeignKey(Trxs,on_delete=models.CASCADE)
