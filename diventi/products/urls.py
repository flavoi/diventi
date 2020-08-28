from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ProductDetailView, 
    AddToUserCollectionView, 
    DropFromUserCollectionView, 
    SecretFileView,
    stripe_webhook,
    CheckoutDoneTemplateView,
    CheckoutFailedTemplateView,
)

app_name = 'products'

urlpatterns = [
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path(_('<slug:slug>/detail/'), ProductDetailView.as_view(), name='detail'),
    path(_('<slug:slug>/add/'), AddToUserCollectionView.as_view(), name='add'),
    path(_('<slug:slug>/remove/'), DropFromUserCollectionView.as_view(), name='drop'),
    path(_('<slug:slug>/secretfile/'), SecretFileView.as_view(), name='secretfile'),
    path(_('<slug:slug>/checkout/done/'), CheckoutDoneTemplateView.as_view(), name='checkout_done'),
    path(_('<slug:slug>/checkout/failed/'), CheckoutFailedTemplateView.as_view(), name='checkout_failed'),
]