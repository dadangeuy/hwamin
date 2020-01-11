from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import RetrieveProfileService
from games.services import GameCommandService


class WebhookUserMessageView(APIView):

    def post(self, request: Request, user_id: str) -> Response:
        session = request.session
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']
        source_id = event['source']['userId']

        if message_type == 'text':
            text = event['message']['text']
            profile = RetrieveProfileService.run(user_id=user_id)
            GameCommandService.run(session, token, text, source_id, profile)

        return Response(None, HTTP_200_OK)
