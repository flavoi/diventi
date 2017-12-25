from django.conf.urls import url
from .views import ProductDetailView, AddToUserCollectionView, DropFromUserCollectionView

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/add/$', AddToUserCollectionView.as_view(), name='add'),
    url(r'^(?P<slug>[-\w]+)/remove/$', DropFromUserCollectionView.as_view(), name='drop'),
]