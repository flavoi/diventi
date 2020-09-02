from django.conf.urls import url
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import (
    DiventiLoginView, 
    DiventiLogoutView, 
    change_password_ajax, 
    change_privacy_ajax, 
    DiventiUserCreationView, 
    DiventiUserUpdateView, 
    DiventiUserPasswordChangeView,
    DiventiUserPrivacyChangeView,
    DiventiUserDetailView, 
    DiventiUserDeleteView, 
    EmailPageView,
    DiventiPasswordResetView,
    DiventiPasswordResetDoneView,
    DiventiPasswordResetConfirmView,
    DiventiPasswordResetCompleteView,
    DiventiUserDetailRedirectView,
)

app_name = 'accounts'

urlpatterns = [
    url(_(r'^signin/$'), DiventiLoginView.as_view(), name='signin'),
    url(_(r'^signout/$'), DiventiLogoutView.as_view(), name='signout'),
    url(_(r'^signup/$'), DiventiUserCreationView.as_view(), name='signup'),
    url(_(r'^change-password/ajax/$'), change_password_ajax, name='change_password_ajax'),    
    url(_(r'^privacy-change/ajax/$'), change_privacy_ajax, name='change_privacy_ajax'),
    url(_(r'^password-reset/$'), DiventiPasswordResetView.as_view(), name='password_reset'),
    url(_(r'^password-reset/done/$'), DiventiPasswordResetDoneView.as_view(), name='password_reset_done'),
    url(_(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'), DiventiPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(_(r'^reset/done/$'), DiventiPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(_(r'^subscribers/$'), EmailPageView.as_view(), name='subscribers'),
    path(_('<int:pk>/'), DiventiUserDetailRedirectView.as_view(), name='redirect'),
    path(_('<slug:nametag>/'), DiventiUserDetailView.as_view(), name='detail'),
    path(_('<slug:nametag>/settings/'), DiventiUserUpdateView.as_view(), name='settings'),
    path(_('<slug:nametag>/update/'), DiventiUserUpdateView.as_view(), name='update'),
    path(_('<slug:nametag>/change-password/'), DiventiUserPasswordChangeView.as_view(), name='change_password'),
    path(_('<slug:nametag>/change-privacy/'), DiventiUserPrivacyChangeView.as_view(), name='change_privacy'),
    path(_('<slug:nametag>/delete/'), DiventiUserDeleteView.as_view(), name='delete'),
]