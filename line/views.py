from logging import getLogger

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

LOG = getLogger(__name__)


class WebhookAPI(APIView):
    def post(self, request: Request) -> Response:
        return Response(None, HTTP_200_OK)
