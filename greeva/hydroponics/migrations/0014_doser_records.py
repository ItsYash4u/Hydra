from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hydroponics", "0013_schema_synced"),
    ]

    operations = [
        migrations.CreateModel(
            name="DoserRecord",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("source_id", models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ("payload", models.JSONField()),
                ("source_timestamp", models.DateTimeField(blank=True, null=True)),
                ("received_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "doser_records",
                "verbose_name": "Doser Record",
                "verbose_name_plural": "Doser Records",
            },
        ),
        migrations.AddIndex(
            model_name="doserrecord",
            index=models.Index(fields=["source_id"], name="doser_src_idx"),
        ),
        migrations.AddIndex(
            model_name="doserrecord",
            index=models.Index(fields=["-source_timestamp"], name="doser_ts_idx"),
        ),
        migrations.AddIndex(
            model_name="doserrecord",
            index=models.Index(fields=["-received_at"], name="doser_rcv_idx"),
        ),
    ]
