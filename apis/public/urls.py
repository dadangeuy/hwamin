from django.urls import path

from apis.public.views import WebhookAPI, WebhookUserAPI, WebhookGroupAPI, WebhookRoomAPI

urlpatterns = [
    path('webhook/', WebhookAPI.as_view()),
    path('webhook/users/<str:user_id>/', WebhookUserAPI.as_view(), name='webhook-user-api'),
    path('webhook/groups/<str:group_id>/', WebhookGroupAPI.as_view(), name='webhook-group-api'),
    path('webhook/rooms/<str:room_id>/', WebhookRoomAPI.as_view(), name='webhook-room-api')
]
