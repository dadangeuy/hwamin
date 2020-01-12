from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.application import AccountApplication
from command.application import CommandApplication


class WebhookUserMessageView(APIView):

    def post(self, request: Request, user_id: str) -> Response:
        event = request.data
        token = event['replyToken']
        message_type = event['message']['type']
        source_id = event['source']['userId']

        if message_type == 'text':
            profile = AccountApplication.get_profile(user_id=user_id)
            text = event['message']['text']
            CommandApplication.run_command(token, source_id, profile.id, text)

        return Response(None, HTTP_200_OK)
