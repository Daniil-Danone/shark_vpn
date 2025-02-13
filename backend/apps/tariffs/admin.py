from django.contrib import admin
from apps.tariffs.models import Tariff, Receipt


class TariffAdmin(admin.ModelAdmin):
    list_display = (
        "title", "price", "duration_value", "duration_type", "is_vip", "partner_bonuses",
    )


class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "tariff", "status", "payment_id", "created_at", "payed_at", "cancelled_at", 
    )


admin.site.register(Tariff, TariffAdmin)
admin.site.register(Receipt, ReceiptAdmin)
