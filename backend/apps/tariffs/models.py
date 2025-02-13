from django.db import models

from apps.users.models import User


class Tariff(models.Model):
    DURATION_CHOICES = [
        ("days", "Дни"),
        ("weeks", "Недели"),
        ("months", "Месяцы"),
        ("years", "Года")
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    title = models.CharField(
        verbose_name="Название", blank=False, null=False
    )

    price = models.DecimalField(
        verbose_name="Цена", max_digits=10, decimal_places=2, blank=False, null=False
    )

    partner_bonuses = models.PositiveIntegerField(
        verbose_name="Количество бонусов для партнёра при оплате", default=0
    )

    is_vip = models.BooleanField(
        verbose_name="VIP статус", default=False
    )

    duration_value = models.PositiveIntegerField(
        verbose_name="Длительность", blank=False, null=False
    )

    duration_type = models.CharField(
        verbose_name="Период", choices=DURATION_CHOICES, default="days"
    )

    is_active = models.BooleanField(
        verbose_name="Активен", default=True
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "💵 Тариф"
        verbose_name_plural = "💵 Тарифы"


class Receipt(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("done", "✅ Оплачено"),
        ("balance", "💰 Списано с баланса"),
        ("wait", "🕒 Ожидает оплаты"),
        ("cancel", "❌ Отклонён"),
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, blank=False, null=True, related_name="user_receipts"
    )

    tariff = models.ForeignKey(
        Tariff, verbose_name="Тариф", on_delete=models.SET_NULL, blank=False, null=True, related_name="tariff_receipts"
    )

    status = models.CharField(
        verbose_name="Статус оплаты", choices=PAYMENT_STATUS_CHOICES, default="wait", max_length=10
    )

    payment_id = models.CharField(
        verbose_name="ID платежа", blank=True, null=True
    )

    payed_at = models.DateTimeField(
        verbose_name="Дата оплаты", blank=True, null=True
    )

    cancelled_at = models.DateTimeField(
        verbose_name="Дата отмены операции", blank=True, null=True
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, null=True
    )

    def __str__(self):
        return f"Операция от {self.created_at.strftime('%d.%m.%Y %H:%M:%S')} - {self.status}"
    
    class Meta:
        verbose_name = "📃 Оплата конфига"
        verbose_name_plural = "📃 Оплаты конфигов"