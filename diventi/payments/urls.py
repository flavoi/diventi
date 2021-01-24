from django.urls import path

from .views import (
    stripe_webhook,
)

app_name = 'payments'

urlpatterns = [
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
]