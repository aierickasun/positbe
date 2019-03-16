# Generated by Django 2.1.7 on 2019-03-10 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20190310_0628'),
        ('stores', '0002_stores_local_tax'),
        ('inventories', '0004_auto_20190310_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventories',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Items'),
        ),
        migrations.AlterUniqueTogether(
            name='inventories',
            unique_together={('item', 'store')},
        ),
    ]