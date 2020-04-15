from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    StorySituationCreateView,
    LandingView,
)

app_name = 'adventures'

urlpatterns = [
    path(_('new-game/'), StorySituationCreateView.as_view(), name='new-game'),
    path('', LandingView.as_view(), name='landing'),    
]