from django.contrib import admin
from apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id", "full_name", "username", "created_at"
    )


admin.site.register(User, UserAdmin)
