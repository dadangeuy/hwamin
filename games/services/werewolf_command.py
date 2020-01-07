from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from commons.patterns import Runnable


class WerewolfCommandService(Runnable):

    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, profile: Profile) -> None: ...
