from django.conf.urls import url

from .views import landing

urlpatterns = [
    url(r'^$', landing, name='home'),
]