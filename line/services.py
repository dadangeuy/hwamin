from json import dumps

from requests import post, get

from accounts.models import Profile
from commons.patterns import Runnable
from hwamin.settings import LINE_ACCESS_TOKEN


class CreateReplyLineService(Runnable):
    API = 'https://api.line.me/v2/bot/message/reply'
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
        response = post(cls.API, dumps(data), headers=cls.HEADERS)
        response.raise_for_status()


class RetrieveProfileLineService(Runnable):
    API = 'https://api.line.me/v2/bot/profile/{0}'
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }

    @classmethod
    def run(cls, profile_id: str) -> Profile:
        response = get(cls.API.format(profile_id), headers=cls.HEADERS)
        response.raise_for_status()
        data = response.json()
        return Profile(id=data['userId'], name=data['displayName'], picture=data['pictureUrl'])
