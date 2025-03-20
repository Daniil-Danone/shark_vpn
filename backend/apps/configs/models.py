from django.db import models
from apps.users.models import User
from apps.tariffs.models import Tariff, Receipt


class Config(models.Model):
    STATUS_CHOICES = [
        ("enable", "✅ Активен"),
        ("disable", "❌ Неактивен"),
    ]

    CONNECT_STATUS_CHOICES = [
        ("connected", "✅ Подключен"),
        ("disconnected", "❌ Отключён"),
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, blank=False, null=True, related_name="user_configs"
    )

    tariff = models.ForeignKey(
        Tariff, verbose_name="Тариф", on_delete=models.SET_NULL, blank=False, null=True, related_name="tariff_configs"
    )

    receipt = models.ForeignKey(
        Receipt, verbose_name="Операция", on_delete=models.SET_NULL, blank=False, null=True, related_name="receipt_configs"
    )

    status = models.CharField(
        verbose_name="Статус активности", choices=STATUS_CHOICES, default="enable", max_length=10
    )

    active = models.CharField(
        verbose_name="Статус подключения", choices=CONNECT_STATUS_CHOICES, default="disconnected", max_length=12
    )

    config_name = models.CharField(
        verbose_name="Название конфига", blank=True, null=True
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, null=True
    )

    expiring_at = models.DateField(
        verbose_name="Дата окончания тарифа", blank=True, null=True
    )

    payment_method_id = models.CharField(
        verbose_name="ID метод оплаты", blank=True, null=True
    )

    is_sub = models.BooleanField(
        verbose_name="Подписка активна", default=True
    )

    def __str__(self):
        return f"Оплата от {self.created_at.strftime('%d.%m.%Y %H:%M:%S')} - {self.status}"
    

    class Meta:
        verbose_name = "📝 Конфиг"
        verbose_name_plural = "📝 Конфиги"
