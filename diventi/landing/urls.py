from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import landing

urlpatterns = [
    url(r'^$', landing, name='home'),
]