# Generated by Django 2.1.7 on 2019-03-10 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0003_auto_20190309_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventories',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
