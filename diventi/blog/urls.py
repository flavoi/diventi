from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import ArticlesListView, ArticleDetailView, ArticlePromoteToggleView, ArticlePromoteToggleAPIView

app_name = 'blog'

urlpatterns = [
    url(r'^$', ArticlesListView.as_view(), name='home'),
    url(_(r'^(?P<slug>[-\w]+)/$'), ArticleDetailView.as_view(), name='detail'),
    url(_(r'^(?P<slug>[-\w]+)/promote/$'), ArticlePromoteToggleView.as_view(), name='promote-toggle'),
    url(_(r'^(?P<slug>[-\w]+)/promote/api/$'), ArticlePromoteToggleAPIView.as_view(), name='promote-toggle-api'),
]