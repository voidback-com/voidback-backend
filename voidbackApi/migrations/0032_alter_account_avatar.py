# Generated by Django 5.1.1 on 2025-04-05 11:39

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("voidbackApi", "0031_alter_account_avatar_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="avatar",
            field=django_resized.forms.ResizedImageField(
                crop=None,
                force_format="PNG",
                keep_meta=True,
                null=True,
                quality=100,
                scale=1,
                size=[320, 320],
                upload_to="avatars/",
            ),
        ),
    ]
