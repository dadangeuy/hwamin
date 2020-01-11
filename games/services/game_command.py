from django.contrib.sessions.backends.base import SessionBase

from accounts.models import Profile
from chats.services import CreateTextReplyService
from commons.patterns import Runnable
from .dua_empat_command import DuaEmpatCommandService
from .play import PlayService
from ..models import Play


class GameCommandService(Runnable):
    @classmethod
    def run(
            cls,
            token: str,
            text: str,
            source_id: str,
            profile: Profile
    ) -> None:
        text = text.lower()
        game_id = PlayService.get_game_id(source_id)
        is_play = game_id is not None

        if not is_play and text == 'menu':
            CreateTextReplyService.run(token, ['main 24', 'main werewolf'])
        elif (not is_play and text == 'main 24') or (game_id == Play.Game.DUA_EMPAT):
            DuaEmpatCommandService.run(token, text, source_id, profile)
