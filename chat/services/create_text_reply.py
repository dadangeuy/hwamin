from typing import List

from rapidjson import dumps
from requests import post

from common.patterns import Runnable
from hwamin.settings import CHANNEL_ACCESS_TOKEN


class CreateTextReplyService(Runnable):
    API = 'https://api.line.me/v2/bot/message/reply'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    @classmethod
    def run(cls, token: str, text_messages: List[str], notification: bool = True) -> None:
        has_message = text_messages is not None and len(text_messages) > 0
        if has_message:
            messages = [{'type': 'text', 'text': text} for text in text_messages]
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
