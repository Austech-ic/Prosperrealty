# Generated by Django 4.2.13 on 2025-01-11 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_dashboard", "0012_alter_additionalinformation_propertystatus_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="additionalinformation",
            name="propertyStatus",
        ),
        migrations.RemoveField(
            model_name="product",
            name="productStatus",
        ),
        migrations.AddField(
            model_name="product",
            name="propertyStatus",
            field=models.CharField(
                blank=True,
                choices=[
                    ("available", "Available"),
                    ("sold", "Sold"),
                    ("rented", "Rented"),
                    ("reserved", "Reserved"),
                    ("not_available", "Not Available"),
                ],
                default="available",
                max_length=500,
                null=True,
            ),
        ),
    ]
