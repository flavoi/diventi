from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ProductListView,
    ProductListViewByCategory,
    ProductDetailView, 
    AddToUserCollectionView, 
    DropFromUserCollectionView, 
    SecretFileView,
    CheckoutDoneTemplateView,
    CheckoutFailedTemplateView,
    RedirectToPublicEbookView,
)

app_name = 'products'

urlpatterns = [
    path(_(''), ProductListView.as_view(), name='list'),
    path(_('category/<slug:category>/'), ProductListViewByCategory.as_view(), name='list_category'),
    path(_('<slug:slug>/'), ProductDetailView.as_view(), name='detail'),
    path(_('<slug:slug>/add/'), AddToUserCollectionView.as_view(), name='add'),
    path(_('<slug:slug>/remove/'), DropFromUserCollectionView.as_view(), name='drop'),
    path(_('<slug:slug>/public-view/'), RedirectToPublicEbookView.as_view(), name='public_view'),
    path(_('<slug:slug>/secretfile/'), SecretFileView.as_view(), name='secretfile'),
    path(_('<slug:slug>/checkout/done/'), CheckoutDoneTemplateView.as_view(), name='checkout_done'),
    path(_('<slug:slug>/checkout/failed/'), CheckoutFailedTemplateView.as_view(), name='checkout_failed'),
]