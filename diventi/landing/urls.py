from django.conf.urls import url

from .views import landing, PresentationDetailView

urlpatterns = [
    url(r'^$', landing, name='home'),
    url(r'^presentation/(?P<pk>\d+)/$', PresentationDetailView.as_view(), name='presentation'),
]