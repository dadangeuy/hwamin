from django.urls import path

from apis.public.views import WebhookAPI, WebhookUserMessageAPI, WebhookGroupMessageAPI, WebhookRoomMessageAPI

urlpatterns = [
    path('webhook/', WebhookAPI.as_view()),
    path(
        'webhook/users/<str:user_id>/events/message/',
        WebhookUserMessageAPI.as_view(),
        name='webhook-user-message-api'
    ),
    path(
        'webhook/groups/<str:group_id>/events/message/',
        WebhookGroupMessageAPI.as_view(),
        name='webhook-group-message-api'
    ),
    path(
        'webhook/rooms/<str:room_id>/events/message/',
        WebhookRoomMessageAPI.as_view(),
        name='webhook-room-message-api'
    ),
]
