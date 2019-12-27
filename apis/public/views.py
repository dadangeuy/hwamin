from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import RetrieveProfileService
from externals.services import CreateReplyLineService


class WebhookAPI(APIView):
    def post(self, request: Request) -> Response:
        events = request.data['events']
        is_verification = events[0]['replyToken'] == '00000000000000000000000000000000'

        if not is_verification:
            for event in events:
                profile_id = event['source']['userId']
                profile = RetrieveProfileService.run(profile_id=profile_id)

                token = event['replyToken']
                text = event['message']['profile']
                reply_text = eval(text)
                CreateReplyLineService.run(token, [reply_text])

        return Response(None, HTTP_200_OK)
