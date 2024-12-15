from datetime import date
from django.db import models


class User(models.Model):
    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    user_id = models.BigIntegerField(
        verbose_name="Telegram ID", unique=True
    )

    full_name = models.CharField(
        verbose_name="Имя", null=False, blank=False
    )

    username = models.CharField(
        verbose_name="Юзернейм", null=True, blank=True
    )

    earned = models.FloatField(
        verbose_name="Заработано", null=True, blank=True, default=0.00
    )

    balance = models.FloatField(
        verbose_name="Баланс", null=True, blank=True, default=0.00
    )

    created_at = models.DateTimeField(
        verbose_name="Дата регистрации", auto_now_add=True, null=True
    )

    def __str__(self):
        return f"Пользователь: {self.user_id}"
    
    class Meta:
        verbose_name = "👤 Пользователь"
        verbose_name_plural = "👤 Пользователи"
