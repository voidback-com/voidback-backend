# Generated by Django 5.1.1 on 2025-03-08 01:10

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0012_datasetcategory_datasetfile_datasetthumbnail_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="files",
        ),
        migrations.AddField(
            model_name="dataset",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dataset",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="datasetfile",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2025, 3, 8, 1, 10, 40, 765102, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datasetfile",
            name="dataset",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="voidbackApi.dataset",
            ),
        ),
        migrations.AddField(
            model_name="datasetfile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="dataset",
            name="name",
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
