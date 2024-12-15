# Generated by Django 5.1.2 on 2024-12-15 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("cash_in", "💰 Пополнение"),
                            ("cash_out", "💸 Вывод"),
                        ],
                        verbose_name="Тип операции",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[("usdt", "💲 USDT"), ("card", "💳 Карта")],
                        verbose_name="Метод",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("done", "✅ Оплачено"),
                            ("wait", "🕒 Ожидает"),
                            ("cancel", "❌ Отклонён"),
                        ],
                        default="wait",
                        max_length=10,
                        verbose_name="Статус операции",
                    ),
                ),
                (
                    "wallet",
                    models.CharField(
                        blank=True, null=True, verbose_name="Кошелёк / номер карты"
                    ),
                ),
                ("amount", models.FloatField(verbose_name="Сумма")),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата совершения операции"
                    ),
                ),
                (
                    "cancelled_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата отмены операции"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания чека"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="operations",
                        to="users.user",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "🪙 Операция",
                "verbose_name_plural": "🪙 Операции",
            },
        ),
    ]
