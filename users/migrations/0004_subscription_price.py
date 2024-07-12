# Generated by Django 5.0.6 on 2024-07-08 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=5.0, max_digits=4, verbose_name="Цена"
            ),
        ),
    ]