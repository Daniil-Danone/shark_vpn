from django.contrib import admin

from apps.operations.models import Operation


class OperationAdmin(admin.ModelAdmin):
    list_display = (
        "type", "method", "status", "amount", "user", "completed_at", "created_at",
    )

    list_filter = (
        "type", "method", "status",
    )

    search_fields = (
        "wallet", "user__full_name", "user__username", 
    )

    readonly_fields = (
        "type", "method", "status", "user", "wallet", "amount", 
        "payment_id", "completed_at", "cancelled_at", "created_at"
    )


admin.site.register(Operation, OperationAdmin)