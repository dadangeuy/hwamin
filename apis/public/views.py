from typing import List

from requests import post, Response as APIResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from externals.services import CreateReplyLineService


class WebhookAPI(APIView):
    def post(self, request: Request) -> Response:
        events = request.data['events']
        is_verification = events[0]['replyToken'] == '00000000000000000000000000000000'
        if not is_verification:
            self.forward_events(request, events)

        return Response(None, HTTP_200_OK)

    def forward_events(self, request: Request, events: list) -> List[APIResponse]:
        return [
            self.forward_event(request, event)
            for event in events
        ]

    def forward_event(self, request: Request, event: dict) -> APIResponse:
        source_type = event['source']['type']
        source_id = (
            event['source']['groupId'] if source_type == 'group' else
            event['source']['roomId'] if source_type == 'room' else
            event['source']['userId']
        )
        url = reverse(f'webhook-{source_type}-api', [source_id], request=request)

        return post(url, event)


class WebhookUserAPI(APIView):
    def post(self, request: Request, user_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        CreateReplyLineService.run(token, [f'User API {user_id}'])

        return Response(None, HTTP_200_OK)


class WebhookGroupAPI(APIView):
    def post(self, request: Request, group_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        CreateReplyLineService.run(token, [f'Group API {group_id}'])

        return Response(None, HTTP_200_OK)


class WebhookRoomAPI(APIView):
    def post(self, request: Request, room_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        CreateReplyLineService.run(token, [f'Room API {room_id}'])

        return Response(None, HTTP_200_OK)
