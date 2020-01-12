from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from requests import get

from account.models import Profile
from common.patterns import Runnable
from hwamin.settings import CHANNEL_ACCESS_TOKEN


class GetOrCreateProfileService(Runnable):
    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    USER_API = 'https://api.line.me/v2/bot/profile/{0}'
    GROUP_API = 'https://api.line.me/v2/bot/group/{0}/member/{1}'
    ROOM_API = 'https://api.line.me/v2/bot/room/{0}/member/{1}'

    @classmethod
    @transaction.atomic
    def run(cls, user_id: str, group_id: str = None, room_id: str = None) -> Profile:
        try:
            return Profile.objects.get(id=user_id)
        except ObjectDoesNotExist:
            data = (
                cls._get_user_from_group(group_id, user_id) if group_id is not None else
                cls._get_user_from_room(room_id, user_id) if room_id is not None else
                cls._get_user(user_id)
            )
            profile = Profile(id=data['userId'], name=data['displayName'], picture=data['pictureUrl'])
            profile.save(force_insert=True)

            return profile

    @classmethod
    def _get_user(cls, user_id: str) -> dict:
        response = get(cls.USER_API.format(user_id), headers=cls.HEADERS)
        response.raise_for_status()
        return response.json()

    @classmethod
    def _get_user_from_group(cls, group_id: str, user_id: str) -> dict:
        response = get(cls.GROUP_API.format(group_id, user_id), headers=cls.HEADERS)
        response.raise_for_status()
        return response.json()

    @classmethod
    def _get_user_from_room(cls, room_id: str, user_id: str) -> dict:
        response = get(cls.ROOM_API.format(room_id, user_id), headers=cls.HEADERS)
        response.raise_for_status()
        return response.json()
