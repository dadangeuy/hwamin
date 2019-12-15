from django.urls import path

from webhooks.views import WebhookAPI

urlpatterns = [
    path('', WebhookAPI.as_view())
]
