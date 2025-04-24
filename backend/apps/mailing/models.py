from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Mail(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = CKEditor5Field(
        verbose_name="Содержание рассылки",
        max_length=4096,
        config_name="default"
    )
    scheduled_time = models.DateTimeField(verbose_name="Расписание отправки")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    completed = models.BooleanField(verbose_name="Выполнено", default=False)

    class Meta:
        verbose_name = "✉️ Рассылка"
        verbose_name_plural = "✉️ Рассылки"

    def __str__(self):
        return f"{self.title} ({self.scheduled_time}) completed: {self.completed}"
