from django.db import models
from vendors.models import Vendors

class Items(models.Model):

    item_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=12)
    vendor = models.ForeignKey('vendors.Vendors',on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

# Create your models here.
