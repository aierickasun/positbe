from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trxs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trxs',
            old_name='store_id',
            new_name='store',
        ),
    ]
    