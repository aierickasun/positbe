from django.db import models

class Prices(models.Model):
    
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=12)
    vendor = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

# Create your models here.
