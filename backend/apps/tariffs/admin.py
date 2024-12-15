from django.contrib import admin
from apps.tariffs.models import Tariff


class TariffAdmin(admin.ModelAdmin):
    list_display = (
        "title", "price", "duration_value", "duration_type", "is_vip"
    )


admin.site.register(Tariff, TariffAdmin)
