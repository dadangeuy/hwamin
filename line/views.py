from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.fields import CharField
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.services import BulkCreateLineAccountService
from commons.serializers import ReadOnlySerializer
from line.services import TextReplyService


class WebhookAPI(APIView):
    class InputSerializer(ReadOnlySerializer):
        token = CharField(source='replyToken')
        line_id = CharField(source='source.userId')

    @transaction.atomic(savepoint=False)
    def post(self, request: Request) -> Response:
        events = request.data['events']

        line_ids = [event['source']['userId'] for event in events]
        BulkCreateLineAccountService.run(line_ids=line_ids)

        tokens = [event['replyToken'] for event in events]
        [TextReplyService.run(token, [f'Halo {token}']) for token in tokens]

        return Response(None, HTTP_200_OK)
