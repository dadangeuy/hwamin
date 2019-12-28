from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import RetrieveProfileService
from games.services import GameCommandService


class WebhookGroupMessageView(APIView):

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
