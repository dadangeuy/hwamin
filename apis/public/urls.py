from django.urls import path

from apis.public.views import WebhookView, WebhookUserMessageView, WebhookGroupMessageView, WebhookRoomMessageView

urlpatterns = [
    path('webhook/', WebhookView.as_view()),
    path(
        'webhook/users/<str:user_id>/events/message/',
        WebhookUserMessageView.as_view(),
        name='webhook-user-message'
    ),
    path(
        'webhook/groups/<str:group_id>/events/message/',
        WebhookGroupMessageView.as_view(),
        name='webhook-group-message'
    ),
    path(
        'webhook/rooms/<str:room_id>/events/message/',
        WebhookRoomMessageView.as_view(),
        name='webhook-room-message'
    ),
]
