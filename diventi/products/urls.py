from django.conf.urls import url
from .views import ProductDetailView, UserCollectionUpdateView

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', UserCollectionUpdateView.as_view(), name='update'),
]