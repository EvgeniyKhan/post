# Generated by Django 5.0.6 on 2024-07-11 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_rename_owner_subscription_payments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="payments",
        ),
        migrations.AddField(
            model_name="user",
            name="payments",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.subscription",
                verbose_name="Ссылка на пользователя",
            ),
        ),
    ]
