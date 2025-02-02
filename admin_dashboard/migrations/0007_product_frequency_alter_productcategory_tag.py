# Generated by Django 4.2.13 on 2025-01-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_dashboard", "0006_productcategory_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="frequency",
            field=models.CharField(
                blank=True,
                choices=[("yearly", "yearly"), ("monthly", "monthly")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="productcategory",
            name="tag",
            field=models.ManyToManyField(blank=True, to="admin_dashboard.producttag"),
        ),
    ]
