from django.contrib import admin
from apps.configs.models import Config


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "user", "tariff", "payment_status", "status", "payed_at", "config_name", "expiring_at", "created_at"
    )


admin.site.register(Config, ConfigAdmin)
