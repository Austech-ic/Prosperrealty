# Generated by Django 4.2.13 on 2025-01-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_remove_user_role_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ManyToManyField(to="account.role"),
        ),
    ]
