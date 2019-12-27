from django.urls import path

from apis.public.views import WebhookAPI

urlpatterns = [
    path('webhook/', WebhookAPI.as_view())
]
