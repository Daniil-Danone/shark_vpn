from django.db import models
from apps.users.models import User
from apps.tariffs.models import Tariff

class Config(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("done", "✅ Оплачено"),
        ("balance", "💰 Списано с баланса"),
        ("wait", "🕒 Ожидает оплаты"),
        ("cancel", "❌ Отклонён"),
    ]

    STATUS_CHOICES = [
        ("enable", "✅ Активен"),
        ("disable", "❌ Неактивен"),
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, blank=False, null=True, related_name="configs"
    )

    tariff = models.ForeignKey(
        Tariff, verbose_name="Тариф", on_delete=models.SET_NULL, blank=False, null=True, related_name="configs"
    )

    payment_status = models.CharField(
        verbose_name="Статус оплаты", choices=PAYMENT_STATUS_CHOICES, default="wait", max_length=10
    )

    status = models.CharField(
        verbose_name="Статус", choices=STATUS_CHOICES, default="disable", max_length=10
    )

    config_name = models.CharField(
        verbose_name="Название конфига", blank=True, null=True
    )

    payed_at = models.DateTimeField(
        verbose_name="Дата оплаты", blank=True, null=True
    )

    cancelled_at = models.DateTimeField(
        verbose_name="Дата отмены операции", blank=True, null=True
    )

    expiring_at = models.DateField(
        verbose_name="Дата окончания тарифа", blank=True, null=True
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, null=True
    )

    def __str__(self):
        return f"Оплата от {self.created_at.strftime('%d.%m.%Y %H:%M:%S')} - {self.status}"
    

    class Meta:
        verbose_name = "📝 Конфиг"
        verbose_name_plural = "📝 Конфиги"
