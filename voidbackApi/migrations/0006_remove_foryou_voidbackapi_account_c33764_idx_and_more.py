# Generated by Django 5.1.1 on 2025-02-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0005_alter_edgeroom_categories"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="foryou",
            name="voidbackApi_account_c33764_idx",
        ),
        migrations.AddField(
            model_name="foryou",
            name="categories",
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name="foryou",
            name="rooms",
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name="post",
            name="title",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="foryou",
            index=models.Index(
                fields=[
                    "account",
                    "symbols",
                    "hashtags",
                    "accounts",
                    "categories",
                    "rooms",
                    "created_at",
                    "updated_at",
                ],
                name="voidbackApi_account_37e9de_idx",
            ),
        ),
    ]
