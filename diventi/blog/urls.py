from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ArticlesListView, 
    ArticlesListViewByCategory,
    ArticleDetailView, 
    ArticlePromoteToggleView, 
    ArticlePromoteToggleAPIView,
)

app_name = 'blog'

urlpatterns = [
    path('', ArticlesListView.as_view(), name='home'),
    path(_('category/<str:category>/'), ArticlesListViewByCategory.as_view(), name='list_category'),
    path(_('article/<slug:slug>/'), ArticleDetailView.as_view(), name='detail'),
    path(_('article/<slug:slug>/promote/'), ArticlePromoteToggleView.as_view(), name='promote-toggle'),
    path(_('article/<slug:slug>/promote/api/'), ArticlePromoteToggleAPIView.as_view(), name='promote-toggle-api'),
]