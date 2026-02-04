from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydroponics', '0010_alter_userdevice_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='Device_Name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Device Name'),
        ),
        migrations.AddField(
            model_name='device',
            name='Device_Type',
            field=models.CharField(choices=[('AIR', 'Air Device'), ('WATER', 'Water Device')], default='AIR', max_length=10, verbose_name='Device Type'),
        ),
        migrations.AddField(
            model_name='device',
            name='Registration_Status',
            field=models.CharField(choices=[('REGISTERED', 'Registered'), ('PENDING', 'Pending')], default='REGISTERED', max_length=20, verbose_name='Registration Status'),
        ),
        migrations.AddField(
            model_name='device',
            name='Registered_At',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Registered At'),
        ),
        migrations.AlterField(
            model_name='device',
            name='Device_ID',
            field=models.CharField(max_length=50, unique=True, verbose_name='Device ID'),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='device',
            index=models.Index(fields=['Device_Type'], name='device_Device_Type_idx'),
        ),
    ]
