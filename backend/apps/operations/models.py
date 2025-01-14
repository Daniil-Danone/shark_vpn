from django.db import models

from apps.users.models import User

class Operation(models.Model):
    STATUS_CHOICES = [
        ("done", "✅ Выполнена"),
        ("wait", "🕒 Ожидает"),
        ("cancel", "❌ Отклонена"),
    ]

    TYPE_CHOICES = [
        ("cash_in", "💰 Пополнение"),
        ("cash_out", "💸 Вывод")
    ]

    METHOD_CHOICES = [
        ("usdt", "💲 USDT"),
        ("card", "💳 Карта")
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    type = models.CharField(
        verbose_name="Тип операции", choices=TYPE_CHOICES, blank=False, null=False
    )

    method = models.CharField(
        verbose_name="Метод", choices=METHOD_CHOICES, blank=False, null=False
    )

    status = models.CharField(
        verbose_name="Статус операции", choices=STATUS_CHOICES, default="wait", max_length=10
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, blank=False, null=True, related_name="operations"
    )

    wallet = models.CharField(
        verbose_name="Кошелёк / номер карты", blank=True, null=True 
    )

    amount = models.FloatField(
        verbose_name="Сумма", blank=False, null=False
    )

    payment_id = models.CharField(
        verbose_name="ID платежа", blank=True, null=True
    )

    completed_at = models.DateTimeField(
        verbose_name="Дата совершения операции", blank=True, null=True
    )

    cancelled_at = models.DateTimeField(
        verbose_name="Дата отмены операции", blank=True, null=True
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания чека", auto_now_add=True
    )

    def __str__(self):
        return f"{self.type} - {self.method} - {self.amount} руб."
    
    class Meta:
        verbose_name = "🪙 Операция"
        verbose_name_plural = "🪙 Операции"
