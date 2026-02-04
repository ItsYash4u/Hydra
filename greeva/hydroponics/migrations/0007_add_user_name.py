from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0006_add_device_owner_and_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdevice',
            name='Name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Full Name'),
        ),
    ]
