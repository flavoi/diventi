from django.contrib import admin
from django.urls import path

from .views import generate_preview

app_name = 'previews'

urlpatterns = [
    path('link/', generate_preview, name='generate'),
]