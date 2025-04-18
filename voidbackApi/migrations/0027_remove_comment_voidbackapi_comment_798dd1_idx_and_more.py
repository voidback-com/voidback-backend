# Generated by Django 5.1.1 on 2025-04-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0026_remove_writeup_voidbackapi_author__9a5a98_idx_and_more"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="comment",
            name="voidbackApi_comment_798dd1_idx",
        ),
        migrations.AddField(
            model_name="comment",
            name="rank",
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["rank", "comment", "writeup", "author", "created_at"],
                name="voidbackApi_rank_2bb2b6_idx",
            ),
        ),
    ]
