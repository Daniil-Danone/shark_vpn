from django.db import models


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