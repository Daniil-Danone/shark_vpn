# Generated by Django 5.1.2 on 2025-01-14 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="operation",
            name="payment_id",
            field=models.CharField(blank=True, null=True, verbose_name="ID платежа"),
        ),
    ]
