from django.conf.urls import url

from .views import DiventiLoginView, DiventiLogoutView, change_password, DiventiUserCreationView, DiventiUserUpdateView

urlpatterns = [
    url(r'^login/$', DiventiLoginView.as_view(), name='login'),
    url(r'^logout/$', DiventiLogoutView.as_view(), name='logout'),
    url(r'^password-change/$', change_password, name='change_password'),
    url(r'^signup/$', DiventiUserCreationView.as_view(), name='signup'),
    url(r'^update/(?P<pk>\d+)/$', DiventiUserUpdateView.as_view(), name='update'),
]