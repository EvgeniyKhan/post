# Generated by Django 5.0.6 on 2024-07-10 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_alter_blog_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blog",
            old_name="user",
            new_name="owner",
        ),
    ]
