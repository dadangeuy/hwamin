from account.models import Profile
from account.services import RetrieveProfileService


class AccountApplication:

    @classmethod
    def retrieve_profile(cls, user_id: str, group_id: str = None, room_id: str = None) -> Profile:
        return RetrieveProfileService.run(user_id, group_id, room_id)
