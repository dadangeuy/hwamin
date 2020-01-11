from rapidjson import dumps
from requests import post

from commons.patterns import Runnable
from hwamin.settings import CHANNEL_ACCESS_TOKEN


class CreateTextReplyService(Runnable):
    API = 'https://api.line.me/v2/bot/message/reply'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    @classmethod
    def run(cls, token: str, texts: list, notification: bool = True) -> None:
        if texts is None or len(texts) == 0:
            return

        messages = [{'type': 'text', 'text': text} for text in texts]
        data = {
            'replyToken': token,
            'messages': messages,
            'notificationDisabled': not notification
        }
        cls._send_request(data)

    @classmethod
    def _send_request(cls, data: dict) -> None:
        data = dumps(data)
        response = post(cls.API, data, headers=cls.HEADERS)
        response.raise_for_status()
