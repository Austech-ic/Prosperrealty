# Generated by Django 4.2.13 on 2025-01-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_dashboard", "0003_remove_product_frequency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productcategory",
            name="tag",
            field=models.ManyToManyField(
                blank=True, related_name="tags", to="admin_dashboard.producttag"
            ),
        ),
    ]
