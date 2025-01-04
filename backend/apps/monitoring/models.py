from django.db import models


class Monitoring(models.Model):
    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    date = models.DateTimeField(
        verbose_name="Дата измерения", auto_now_add=True
    )

    cpu_cores = models.IntegerField(
        verbose_name="Ядра CPU", blank=True, null=True
    )

    cpu_threads = models.IntegerField(
        verbose_name="Потоки CPU", blank=True, null=True
    )

    cpu_usage = models.FloatField(
        verbose_name="Нагрузка на CPU", blank=True, null=True
    )

    usage_per_thread = models.JSONField(
        verbose_name="Нагрузка на ядра", blank=True, null=True
    )

    ram_total = models.IntegerField(
        verbose_name="Всего RAM", blank=True, null=True
    )

    ram_used = models.IntegerField(
        verbose_name="Использовано RAM", blank=True, null=True
    )

    ram_available = models.IntegerField(
        verbose_name="Свободно RAM", blank=True, null=True
    )

    ram_usage = models.FloatField(
        verbose_name="Нагрузка на RAM", blank=True, null=True
    )

    disk_total = models.IntegerField(
        verbose_name="Всего DISK", blank=True, null=True
    )

    disk_used = models.IntegerField(
        verbose_name="Использовано DISK", blank=True, null=True
    )

    disk_available = models.IntegerField(
        verbose_name="Свободно DISK", blank=True, null=True
    )

    disk_usage = models.FloatField(
        verbose_name="Нагрузка на DISK", blank=True, null=True
    )

    def __str__(self):
        return self.date.strftime("%d.%m.%Y %H:%M:%S")
    
    class Meta:
        verbose_name = "Нагрузка"
        verbose_name_plural = "Статистика нагрузки сервера"