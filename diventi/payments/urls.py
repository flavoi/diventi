from django.urls import path

from .views import (
    stripe_webhook,
    create_checkout_session,
)

app_name = 'payments'

urlpatterns = [
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('create-checkout-session/<slug:product_slug>/', create_checkout_session, name='create_checkout_session'),
]