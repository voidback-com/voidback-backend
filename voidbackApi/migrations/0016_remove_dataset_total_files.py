# Generated by Django 5.1.1 on 2025-03-09 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0015_datasetfile_hash"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="total_files",
        ),
    ]
