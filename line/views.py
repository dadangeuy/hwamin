from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.fields import CharField
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from commons.serializers import ReadOnlySerializer


class WebhookAPI(APIView):
    class InputSerializer(ReadOnlySerializer):
        username = CharField(source='source.userId')

    @transaction.atomic(savepoint=False)
    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(request.data['events'], many=True)
        users = [
            User.objects.get_or_create(**datum)
            for datum in serializer.data
        ]
        return Response(None, HTTP_200_OK)
