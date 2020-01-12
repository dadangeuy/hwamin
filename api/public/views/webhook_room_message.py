from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from account.application import AccountApplication
from command.application import CommandApplication


class WebhookRoomMessageView(APIView):

    def post(self, request: Request, room_id: str) -> Response:
        event = request.data
        user_id = event['source']['userId']
        token = event['replyToken']
        message_type = event['message']['type']
        source_id = event['source']['roomId']

        if message_type == 'text':
            profile = AccountApplication.get_profile(user_id=user_id, room_id=room_id)
            text = event['message']['text']
            CommandApplication.run_command(source_id, profile.id, text, token)

        return Response(None, HTTP_200_OK)
