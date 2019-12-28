from json import dumps
from typing import List

from requests import post, Response as APIResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from externals.services import CreateReplyLineService
from games.services import DuaEmpatCalculatorService


class WebhookAPI(APIView):
    HEADERS = {
        'Content-Type': 'application/json'
    }

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

        return post(url, dumps(event), headers=self.HEADERS)


class WebhookUserMessageAPI(APIView):
    def post(self, request: Request, user_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']

        if message_type == 'text':
            text = event['message']['text']
            self.process_text(token, text)

        return Response(None, HTTP_200_OK)

    def process_text(self, token: str, text: str) -> None:
        result = DuaEmpatCalculatorService.run(text)
        is_24 = result == 24
        reply_text = 'Dua Empat!!' if is_24 else f'Kok {result:g} :('
        CreateReplyLineService.run(token, [reply_text])
