from django.contrib import admin
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field

from .models import Mail


class MailForm(forms.ModelForm):
    content = CKEditor5Field()

    class Meta:
        model = Mail
        fields = ["title", "content", "scheduled_time", "completed"]

    def clean_scheduled_time(self):
        scheduled_time = self.cleaned_data.get('scheduled_time')
        if scheduled_time and scheduled_time < timezone.now():
            raise ValidationError("Дата и время рассылки не могут быть в прошлом!")
        return scheduled_time


class MailAdmin(admin.ModelAdmin):
    form = MailForm  # Используем форму с CKEditor5
    list_display = ("title", "scheduled_time", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title", "content")

    fieldsets = (
        (None, {
            "fields": ("title", "content", "scheduled_time", "completed")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ("created_at",)

    def save_model(self, request, obj, form, change):
        if not obj.completed:
            obj.completed = False
        super().save_model(request, obj, form, change)


admin.site.register(Mail, MailAdmin)
