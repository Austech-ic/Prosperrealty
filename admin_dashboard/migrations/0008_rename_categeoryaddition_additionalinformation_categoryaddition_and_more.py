# Generated by Django 4.2.13 on 2025-01-10 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("admin_dashboard", "0007_product_frequency_alter_productcategory_tag"),
    ]

    operations = [
        migrations.RenameField(
            model_name="additionalinformation",
            old_name="categeoryAddition",
            new_name="categoryAddition",
        ),
        migrations.RenameField(
            model_name="specification",
            old_name="categeorySpecification",
            new_name="categorySpecification",
        ),
    ]
