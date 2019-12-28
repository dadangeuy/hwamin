from json import dumps
from typing import List

from requests import Response as APIResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import RetrieveProfileService
from games.services import GameCommandService
from sessions.services import RetrieveSessionService


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
        event_type = event['type']
        url = reverse(f'webhook-{source_type}-{event_type}-api', [source_id], request=request)
        session = RetrieveSessionService.run(source_id)

        return session.post(url, dumps(event))


class WebhookUserMessageAPI(APIView):
    def post(self, request: Request, user_id: str) -> Response:
        session = request.session
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']

        if message_type == 'text':
            text = event['message']['text']
            profile = RetrieveProfileService.run(user_id=user_id)
            GameCommandService.run(session, token, text, profile)

        return Response(None, HTTP_200_OK)


class WebhookGroupMessageAPI(APIView):
    def post(self, request: Request, group_id: str) -> Response:
        session = request.session
        event = request.data
        user_id = event['source']['userId']
        token = event['replyToken']
        message_type = event['message']['type']

        if message_type == 'text':
            profile = RetrieveProfileService.run(user_id=user_id, group_id=group_id)
            text = event['message']['text']
            GameCommandService.run(session, token, text, profile)

        return Response(None, HTTP_200_OK)


class WebhookRoomMessageAPI(APIView):
    def post(self, request: Request, room_id: str) -> Response:
        session = request.session
        event = request.data
        user_id = event['source']['userId']
        token = event['replyToken']
        message_type = event['message']['type']

        if message_type == 'text':
            profile = RetrieveProfileService.run(user_id=user_id, room_id=room_id)
            text = event['message']['text']
            GameCommandService.run(session, token, text, profile)

        return Response(None, HTTP_200_OK)
