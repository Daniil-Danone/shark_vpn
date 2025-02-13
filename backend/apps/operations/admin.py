from django.contrib import admin

from apps.operations.models import Operation


class OperationAdmin(admin.ModelAdmin):
    list_display = (
        "type", "status", "amount", "user", "completed_at", "created_at",
    )

    list_filter = (
        "type", "status",
    )

    search_fields = (
        "wallet", "user__full_name", "user__username", 
    )

    readonly_fields = (
        "type", "status", "user", "wallet", "amount", 
        "payment_id", "completed_at", "cancelled_at", "created_at"
    )

    exclude = (
        "method",
    )


admin.site.register(Operation, OperationAdmin)