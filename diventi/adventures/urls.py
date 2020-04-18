from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    StorySituationCreateView,
    StoryDetailView,
    SituationDetailView,
    LandingView,
)

app_name = 'adventures'

urlpatterns = [
    path(_('new-game/'), StorySituationCreateView.as_view(), name='new-game'),
    path(_('story/<int:pk>/'), StoryDetailView.as_view(), name='story_detail'),
    path(_('situation/<uuid:uuid>/'), SituationDetailView.as_view(), name='situation_detail'), 
    path('', LandingView.as_view(), name='landing'),    
]