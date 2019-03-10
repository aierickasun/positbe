from django.db import models
from stores.models import Stores as stores
from items.models import Items as items

class Inventories(models.Model):
    item = models.OneToOneField(
        items,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(blank=False)
    store = models.ForeignKey(
        stores,
        on_delete=models.CASCADE,
    )
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('id',)

# Create your models here.
