from django.db import models


class FAQTheme(models.Model):
    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    title = models.CharField(
        verbose_name="Название", blank=False, null=False
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "🗂 Тема"
        verbose_name_plural = "🗂 Темы"


class FAQProblem(models.Model):
    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )

    theme = models.ForeignKey(
        FAQTheme, verbose_name="Тема проблемы", on_delete=models.CASCADE
    )

    question = models.CharField(
        verbose_name="Проблема", blank=False, null=False
    )

    solution = models.TextField(
        verbose_name="Решение проблемы", blank=False, null=False
    )

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "❓ Проблема"
        verbose_name_plural = "❓ Проблемы"