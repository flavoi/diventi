from django.conf.urls import url

from .views import DiventiLoginView, DiventiLogoutView

urlpatterns = [
    url(r'^login/$', DiventiLoginView.as_view(), name='login'),
    url(r'^logout/$', DiventiLogoutView.as_view(), name='logout'),
]