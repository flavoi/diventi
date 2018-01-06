from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import ProductDetailView, AddToUserCollectionView, DropFromUserCollectionView

urlpatterns = [
    url(_(r'^(?P<slug>[-\w]+)/$'), ProductDetailView.as_view(), name='detail'),
    url(_(r'^(?P<slug>[-\w]+)/add/$'), AddToUserCollectionView.as_view(), name='add'),
    url(_(r'^(?P<slug>[-\w]+)/remove/$'), DropFromUserCollectionView.as_view(), name='drop'),
]