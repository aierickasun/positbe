# Generated by Django 2.1.7 on 2019-03-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stores',
            name='local_tax',
            field=models.DecimalField(decimal_places=3, default=9.5, max_digits=12),
        ),
    ]
