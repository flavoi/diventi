from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    SituationStoryCreateView,
    SituationStoryDetailView,
    StoryDetailView,
    story_get,
    SituationStoryResolutionView,
)

app_name = 'adventures'

urlpatterns = [
    path(_(''), SituationStoryCreateView.as_view(), name='new-game'),
    path(_('situation/story/<uuid:uuid>/'), SituationStoryDetailView.as_view(), name='situation_detail'),
    path(_('situation/story/<uuid:uuid>/resolution/'), SituationStoryResolutionView.as_view(), name='situation_resolution'),
    path(_('story/<uuid:uuid>/get/'), story_get, name='story_get'),
    path(_('story/<uuid:uuid>/'), StoryDetailView.as_view(), name='story_detail'),   
]