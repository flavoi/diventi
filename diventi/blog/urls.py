from django.conf.urls import url
from .views import ArticlesListView, ArticleDetailView, ArticlePromoteToggleView, ArticlePromoteToggleAPIView

urlpatterns = [
    url(r'^$', ArticlesListView.as_view(), name='home'),
    url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/promote/$', ArticlePromoteToggleView.as_view(), name='promote-toggle'),
    url(r'^(?P<slug>[-\w]+)/promote/api/$', ArticlePromoteToggleAPIView.as_view(), name='promote-toggle-api'),
]