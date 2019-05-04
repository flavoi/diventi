from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import (
    DiventiLoginView, 
    DiventiLogoutView, 
    change_password_ajax, 
    change_privacy_ajax, 
    DiventiUserCreationView, 
    DiventiUserUpdateView, 
    DiventiUserDetailView, 
    DiventiUserDeleteView, 
    EmailPageView,
    DiventiPasswordResetView,
    DiventiPasswordResetDoneView,
    DiventiPasswordResetConfirmView,
    DiventiPasswordResetCompleteView,
    DashboardLoginView,
)

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
    url(_(r'^password-reset/$'), DiventiPasswordResetView.as_view(), name='password_reset'),
    url(_(r'^password-reset/done/$'), DiventiPasswordResetDoneView.as_view(), name='password_reset_done'),
    url(_(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'), DiventiPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(_(r'^reset/done/$'), DiventiPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(_(r'^subscribers/$'), EmailPageView.as_view(), name='subscribers'),
    url(_(r'^login/$'), DashboardLoginView.as_view(), name='login'),
]