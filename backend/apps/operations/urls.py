from django.urls import path
from apps.operations.views import payment_success


urlpatterns = [
    path('payment/success/', payment_success, name='payment_success'),
]