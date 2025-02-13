from django.contrib import admin
from apps.configs.models import Config


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "user", "tariff", "payment_status", "status", "active", 
        "payed_at", "config_name", "expiring_at", "is_sub", "created_at"
    )

    # readonly_fields = (
    #     "user", "tariff", "status", "active", "config_name", 
    #     "payment_id", "payed_at", "cancelled_at", "is_sub", "expiring_at",
    #     "created_at",
    # )


admin.site.register(Config, ConfigAdmin)
