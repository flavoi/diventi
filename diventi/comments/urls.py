from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import CommentPromoteToggleView, CommentPromoteToggleAPIView

urlpatterns = [
    url(_(r'^(?P<pk>\d+)/promote/$'), CommentPromoteToggleView.as_view(), name='promote-toggle'),
    url(_(r'^(?P<pk>\d+)/promote/api/$'), CommentPromoteToggleAPIView.as_view(), name='promote-toggle-api'),
]