from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    StorySituationCreateView,
    StoryDetailView,
    SituationDetailView,
    LandingView,
    get_story,
    situation_next,
)

app_name = 'adventures'

urlpatterns = [
    path(_(''), StorySituationCreateView.as_view(), name='new-game'),
    path(_('situation/<uuid:uuid>/'), SituationDetailView.as_view(), name='situation_detail'),
    path(_('situation/<uuid:uuid>/next'), situation_next, name='situation_next'),
    path(_('get_story/<uuid:story_uuid>/'), get_story, name='get_story'),
    path(_('story/<uuid:uuid>/'), StoryDetailView.as_view(), name='story_detail'),   
]