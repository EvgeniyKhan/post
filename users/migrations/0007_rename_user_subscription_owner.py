# Generated by Django 5.0.6 on 2024-07-10 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_remove_subscription_blog"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subscription",
            old_name="user",
            new_name="owner",
        ),
    ]