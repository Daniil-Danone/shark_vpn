from django.urls import path

from apps.tariffs.views import YoukassaWebhookAPIView


urlpatterns = [
    path("youkassa/webhook", YoukassaWebhookAPIView.as_view()),
]