from json import dumps

from requests import post

from commons.patterns import Runnable
from hwamin.settings import LINE_ACCESS_TOKEN


class TextReplyService(Runnable):
    URL = 'https://api.line.me/v2/bot/message/reply'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }

    @classmethod
    def run(cls, token: str, texts: list, notification: bool = True) -> None:
        messages = [{'type': 'text', 'text': text} for text in texts]
        data = {
            'replyToken': token,
            'messages': messages,
            'notificationDisabled': not notification
        }
        response = post(cls.URL, dumps(data), headers=cls.HEADERS)
        response.raise_for_status()
