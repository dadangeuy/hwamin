from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from chats.services import CreateTextReplyService
from commons.patterns import Runnable
from .dua_empat_command import DuaEmpatCommandService


class GameCommandService(Runnable):
    @classmethod
    def run(
            cls,
            session: SessionBase,
            token: str,
            text: str,
            source_id: str,
            profile: Profile
    ) -> None:
        text = text.lower()
        game = session.get('game', None)
        if game is None and text == 'menu':
            CreateTextReplyService.run(token, ['main 24', 'main werewolf'])
        if (game is None and text == 'main 24') or (game == 'DUA_EMPAT'):
            DuaEmpatCommandService.run(session, token, text, source_id, profile)
