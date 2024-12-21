# Generated by Django 5.1.2 on 2024-12-21 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Referal",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "invited_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата приглашения"
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="referals",
                        to="users.user",
                        verbose_name="Партнёр",
                    ),
                ),
                (
                    "referal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="partner",
                        to="users.user",
                        verbose_name="Реферал",
                    ),
                ),
            ],
            options={
                "verbose_name": "👥 Реферал",
                "verbose_name_plural": "👥 Рефералы",
            },
        ),
    ]
