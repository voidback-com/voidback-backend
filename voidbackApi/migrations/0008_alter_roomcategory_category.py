# Generated by Django 5.1.1 on 2025-02-26 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0007_remove_datahubaccount_account_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roomcategory",
            name="category",
            field=models.TextField(blank=True, max_length=20),
        ),
    ]
