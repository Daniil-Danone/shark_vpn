from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("operations/", include("apps.operations.urls")),
    path("api/v1/payments/", include("apps.tariffs.urls")),
]
