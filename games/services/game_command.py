from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from commons.patterns import Runnable
from games.services import DuaEmpatCommandService


class GameCommandService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, profile: Profile) -> None:
        game = session.get('game', None)
        if (game is None and text is 'main 24') or (game == 'DUA_EMPAT'):
            DuaEmpatCommandService.run(session, token, text, profile)
