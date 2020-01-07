from json import dumps

from requests import post

from commons.patterns import Runnable
from hwamin.settings import LINE_ACCESS_TOKEN


class CreateReplyService(Runnable):
    API = 'https://api.line.me/v2/bot/message/reply'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }

    @classmethod
    def run(cls, data: dict) -> None:
        response = post(cls.API, dumps(data), headers=cls.HEADERS)
        response.raise_for_status()
