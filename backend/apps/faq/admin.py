from django.contrib import admin

from apps.faq.models import FAQTheme, FAQProblem


class FAQProblemInline(admin.StackedInline):
    model = FAQProblem
    extra = 0


class FAQThemeAdmin(admin.ModelAdmin):
    inlines = [FAQProblemInline]
    list_display = (
        "title",
    )


class FAQProblemAdmin(admin.ModelAdmin):
    list_display = (
        "theme", "question",
    )

    list_filter = (
        "theme",
    )


admin.site.register(FAQTheme, FAQThemeAdmin)
admin.site.register(FAQProblem, FAQProblemAdmin)