# Generated by Django 2.1.7 on 2019-03-09 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0002_auto_20190303_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventories',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
