from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from commons.patterns import Runnable
from games.services import StartGameService, DuaEmpatReplyService


class TextService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str, profile: Profile) -> None:
        game = session.get('game', None)
        if game is None:
            StartGameService.run(session, token, text)
        elif game == 'DUA_EMPAT':
            DuaEmpatReplyService.run(session, token, text, profile)
