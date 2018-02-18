from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import DiventiLoginView, DiventiLogoutView, change_password, change_password_ajax, DiventiUserCreationView, DiventiUserUpdateView

urlpatterns = [
    url(_(r'^signin/$'), DiventiLoginView.as_view(), name='signin'),
    url(_(r'^signout/$'), DiventiLogoutView.as_view(), name='signout'),
    url(_(r'^password-change/$'), change_password, name='change_password'),
    url(_(r'^password-change/ajax/$'), change_password_ajax, name='change_password_ajax'),
    url(_(r'^signup/$'), DiventiUserCreationView.as_view(), name='signup'),
    url(_(r'^(?P<pk>\d+)/update/$'), DiventiUserUpdateView.as_view(), name='update'),
]