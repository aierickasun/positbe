# Generated by Django 2.1.7 on 2019-03-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trxs', '0004_auto_20190310_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='trxs',
            name='sale_dollars',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='trxs',
            name='tax_dollars',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]