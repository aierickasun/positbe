from django.db import models

class Stores(models.Model):

    store_name = models.CharField(max_length=100)
    store_address = models.CharField(max_length=100)
    store_city = models.CharField(max_length=100)
    store_state = models.CharField(max_length=100)
    local_tax = models.DecimalField(decimal_places=3,max_digits=12,default=9.5)

    class Meta:
        ordering = ('id',)

# Create your models here.
