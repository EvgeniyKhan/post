# Generated by Django 5.0.6 on 2024-07-08 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_subscription_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="is_subscribed",
            field=models.BooleanField(default=False, verbose_name="Подписка"),
        ),
    ]