from django.db import models
from apps.users.models import User


class Referal(models.Model):
    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    partner = models.ForeignKey(
        User, verbose_name="Партнёр", on_delete=models.SET_NULL, blank=False, null=True, related_name="referals"
    )

    referal = models.ForeignKey(
        User, verbose_name="Реферал", on_delete=models.SET_NULL, blank=False, null=True, related_name="partner"
    )

    invited_at = models.DateTimeField(
        verbose_name="Дата приглашения", auto_now_add=True
    )

    def __str__(self):
        return f"«{self.referal.full_name}» приглашён пользователем «{self.partner.full_name}»"
    
    class Meta:
        verbose_name = "👥 Реферал"
        verbose_name_plural = "👥 Рефералы"