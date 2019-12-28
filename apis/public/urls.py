from django.urls import path

from apis.public.views import WebhookAPI, WebhookUserMessageAPI

urlpatterns = [
    path('webhook/', WebhookAPI.as_view()),
    path(
        'webhook/users/<str:user_id>/events/message/',
        WebhookUserMessageAPI.as_view(),
        name='webhook-user-message-api'
    ),
]
