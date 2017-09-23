from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import landing, DiventiLoginView, DiventiLogoutView

urlpatterns = [
    url(r'^$', landing, name='home'),
    url(r'^login/$', DiventiLoginView.as_view(), name='login'),
    url(r'^logout/$', DiventiLogoutView.as_view(), name='logout'),
]