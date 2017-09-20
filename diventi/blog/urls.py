from django.conf.urls import url
from .views import ArticlesListView, ArticleDetailView

urlpatterns = [
    url(r'^$', ArticlesListView.as_view(), name='home'),
    url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='detail'),
]