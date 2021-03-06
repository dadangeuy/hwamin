from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.client import AccountClient
from command.client import CommandClient


class WebhookGroupMessageView(APIView):

    def post(self, request: Request, group_id: str) -> Response:
        event = request.data
        user_id = event['source']['userId']
        token = event['replyToken']
        message_type = event['message']['type']
        source_id = event['source']['groupId']

        if message_type == 'text':
            profile = AccountClient.get_profile(user_id=user_id, group_id=group_id)
            text = event['message']['text']
            CommandClient.run_command(token, source_id, profile.id, text)

        return Response(None, HTTP_200_OK)
