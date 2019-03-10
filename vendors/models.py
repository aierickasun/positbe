from django.db import models

class Vendors(models.Model):
    vendor_name = models.CharField(max_length = 100)
    vendor_address = models.CharField(max_length = 100)
    vendor_city = models.CharField(max_length = 100)
    vendor_state = models.CharField(max_length = 100)

    class Meta:
        ordering = ('id',)
# Create your models here.
