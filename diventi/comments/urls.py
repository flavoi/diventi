from django.conf.urls import url
from .views import CommentPromoteToggleView, CommentPromoteToggleAPIView

urlpatterns = [
    url(r'^(?P<pk>\d+)/promote/$', CommentPromoteToggleView.as_view(), name='promote-toggle'),
    url(r'^(?P<pk>\d+)/promote/api/$', CommentPromoteToggleAPIView.as_view(), name='promote-toggle-api'),
]