from django.conf.urls import url

from .views import landing, PresentationDetailView, PresentationSearchView

urlpatterns = [
    url(r'^$', landing, name='home'),
    url(r'^presentation/(?P<pk>\d+)/$', PresentationDetailView.as_view(), name='presentation'),
    url(r'^search/$', PresentationSearchView.as_view(), name='search'),
]