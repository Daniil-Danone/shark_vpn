from django.contrib import admin
from apps.configs.models import Config


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        "user", "tariff", "receipt", "is_sub", "status", "active", 
        "config_name", "created_at", "expiring_at",  
    )

    search_fields = (
        "user__full_name", "user__username", "user__user_id", "config_name"
    )

    list_filter = (
        "user", "tariff", "is_sub", "status", "active",
    )

    # readonly_fields = (
    #     "user", "tariff", "status", "active", "config_name", 
    #     "payment_id", "payed_at", "cancelled_at", "is_sub", "expiring_at",
    #     "created_at",
    # )


admin.site.register(Config, ConfigAdmin)
