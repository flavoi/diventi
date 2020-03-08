from django.urls import path

from .views import file_challenge

app_name = 'brave'

urlpatterns = [
    path('brave-rewards-verification.txt/', file_challenge),
]