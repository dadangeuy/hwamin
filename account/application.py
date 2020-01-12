from account.models import Profile
from account.services import GetOrCreateProfileService


class AccountApplication:

    @classmethod
    def get_profile(cls, user_id: str, group_id: str = None, room_id: str = None) -> Profile:
        return GetOrCreateProfileService.run(user_id, group_id, room_id)
