# Generated by Django 4.2.13 on 2025-01-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(null=True),
        ),
    ]
