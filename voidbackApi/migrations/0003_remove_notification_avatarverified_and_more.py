# Generated by Django 5.1.1 on 2025-05-18 06:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0002_remove_writeup_voidbackapi_author__315fc0_idx_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="avatarVerified",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="body",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="fromAvatar",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="fromName",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="fromNameMessage",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="icon",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="navPath",
        ),
        migrations.AddField(
            model_name="notification",
            name="content",
            field=models.JSONField(blank=True, default=[]),
        ),
        migrations.AddField(
            model_name="notification",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="notification",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
