# Generated by Django 5.1.2 on 2025-02-13 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0006_remove_config_cancelled_at_remove_config_payed_at_and_more"),
        ("tariffs", "0003_receipt"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="config",
            name="receipt",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="receipt_configs",
                to="tariffs.receipt",
                verbose_name="Операция",
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="status",
            field=models.CharField(
                choices=[("enable", "✅ Активен"), ("disable", "❌ Неактивен")],
                default="enable",
                max_length=10,
                verbose_name="Статус активности",
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="tariff",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tariff_configs",
                to="tariffs.tariff",
                verbose_name="Тариф",
            ),
        ),
        migrations.AlterField(
            model_name="config",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_configs",
                to="users.user",
                verbose_name="Пользователь",
            ),
        ),
    ]
