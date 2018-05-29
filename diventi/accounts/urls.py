from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import DiventiLoginView, DiventiLogoutView, change_password_ajax, change_privacy_ajax, DiventiUserCreationView, DiventiUserUpdateView, DiventiUserDetailView, DiventiUserDeleteView, EmailPageView

app_name = 'accounts'

urlpatterns = [
    url(_(r'^signin/$'), DiventiLoginView.as_view(), name='signin'),
    url(_(r'^signout/$'), DiventiLogoutView.as_view(), name='signout'),
    url(_(r'^password-change/ajax/$'), change_password_ajax, name='change_password_ajax'),
    url(_(r'^signup/$'), DiventiUserCreationView.as_view(), name='signup'),
    url(_(r'^(?P<pk>\d+)/$'), DiventiUserDetailView.as_view(), name='detail'),
    url(_(r'^(?P<pk>\d+)/update/$'), DiventiUserUpdateView.as_view(), name='update'),
    url(_(r'^privacy-change/ajax/$'), change_privacy_ajax, name='change_privacy_ajax'),
    url(_(r'^(?P<pk>\d+)/delete/$'), DiventiUserDeleteView.as_view(), name='delete'),
    url(_(r'^emails/$'), EmailPageView.as_view(), name='emails'),
]