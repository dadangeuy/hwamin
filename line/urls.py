from django.urls import path

from line.views import WebhookAPI

urlpatterns = [
    path('webhook/', WebhookAPI.as_view())
]
