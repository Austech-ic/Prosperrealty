# Generated by Django 4.2.13 on 2025-01-10 06:10

import admin_dashboard.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=500)),
                (
                    "shortDescription",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("location", models.CharField(max_length=500)),
                ("tourUrl", models.URLField(blank=True, null=True)),
                ("description", models.TextField()),
                (
                    "currency",
                    models.CharField(
                        choices=[("NG", "NG"), ("USD", "USD")],
                        default="NG",
                        max_length=100,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "frequency",
                    models.CharField(
                        blank=True,
                        choices=[("yearly", "yearly"), ("monthly", "monthly")],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Property for sale", "Property for sale"),
                            ("Appartment for sale", "Appartment for sale"),
                            ("3 Bedroom flat", "3 Bedroom flat"),
                        ],
                        max_length=100,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category",
                        to="admin_dashboard.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductTag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=500, null=True)),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Specification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "specificationType",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("sqft", models.CharField(blank=True, max_length=500, null=True)),
                ("bathroom", models.IntegerField(default=0)),
                ("bedroom", models.IntegerField(default=0)),
                ("buildYear", models.DateField(blank=True, null=True)),
                ("others", models.JSONField(default=list)),
                (
                    "packing",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "categeorySpecification",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specification",
                        to="admin_dashboard.productcategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        max_length=500,
                        upload_to=admin_dashboard.models.ProductImage.upload_to,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="admin_dashboard.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="productcategory",
            name="tag",
            field=models.ManyToManyField(blank=True, to="admin_dashboard.producttag"),
        ),
        migrations.CreateModel(
            name="AdditionalInformation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "propertyStaus",
                    models.CharField(
                        blank=True,
                        choices=[("Ongoing", "Ongoing"), ("Completed", "Completed")],
                        max_length=500,
                        null=True,
                    ),
                ),
                (
                    "buildingName",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("deedNumber", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "NeighbourhoodName",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "categeoryAddition",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addition",
                        to="admin_dashboard.productcategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
