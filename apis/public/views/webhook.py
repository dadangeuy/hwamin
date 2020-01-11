from typing import List

from rapidjson import dumps
from requests import Response as APIResponse, post
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class WebhookView(APIView):
    HEADERS = {
        'Content-Type': 'application/json',
    }

    def post(self, request: Request) -> Response:
        events = request.data['events']
        is_verification = events[0]['replyToken'] == '00000000000000000000000000000000'
        if not is_verification:
            self.forward_events(request, events)

        return Response(None, HTTP_200_OK)

    def forward_events(self, request: Request, events: list) -> List[APIResponse]:
        events = [
            self.forward_event(request, event)
            for event in events
        ]
        return events

    def forward_event(self, request: Request, event: dict) -> APIResponse:
        source_type = event['source']['type']
        source_id = (
            event['source']['groupId'] if source_type == 'group' else
            event['source']['roomId'] if source_type == 'room' else
            event['source']['userId']
        )
        event_type = event['type']

        url = reverse(f'webhook-{source_type}-{event_type}', [source_id], request=request)
        data = dumps(event)
        response = post(url, data, headers=self.HEADERS)

        return response
