from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ProductListView,
    ProductListViewByCategory,
    ProductDetailView, 
    AddToUserCollectionView, 
    DropFromUserCollectionView, 
    CheckoutDoneTemplateView,
    CheckoutFailedTemplateView,
    RedirectToPublicEbookView,
    add_public_product_to_user_collection_view,
    checkout_done_pdf,
    user_product_download,
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path(_('category/<slug:category>/'), ProductListViewByCategory.as_view(), name='list_category'),
    path(_('<slug:slug>/'), ProductDetailView.as_view(), name='detail'),
    path(_('<slug:slug>/add/'), AddToUserCollectionView.as_view(), name='add'),
    path(_('<slug:slug>/add/public/'), add_public_product_to_user_collection_view, name='add_public'),
    path(_('<slug:slug>/remove/'), DropFromUserCollectionView.as_view(), name='drop'),
    path(_('<slug:slug>/public/'), RedirectToPublicEbookView.as_view(), name='detail-public'),
    path(_('<slug:slug>/checkout/done/'), CheckoutDoneTemplateView.as_view(), name='checkout_done'),
    path(_('<slug:slug>/checkout/failed/'), CheckoutFailedTemplateView.as_view(), name='checkout_failed'),
    path(_('<slug:slug>/checkout/done/session/<str:session_id>/pdf/'), checkout_done_pdf, name='checkout_done_pdf'),
    path(_('<slug:slug>/download/'), user_product_download, name='user_product_download'),
]