from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import RetrieveProfileService
from games.application import GameApplication


class WebhookUserMessageView(APIView):

    def post(self, request: Request, user_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']
        source_id = event['source']['userId']

        if message_type == 'text':
            text = event['message']['text']
            profile = RetrieveProfileService.run(user_id=user_id)
            GameApplication.run_command(source_id, profile.id, text, token)

        return Response(None, HTTP_200_OK)
