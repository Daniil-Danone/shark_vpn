from django.contrib import admin

from apps.referals.models import Referal

class ReferalAdmin(admin.ModelAdmin):
    list_display = (
        "partner", "referal", "invited_at",
    )

    readonly_fields = (
        "partner", "referal", "invited_at",
    )


admin.site.register(Referal, ReferalAdmin)