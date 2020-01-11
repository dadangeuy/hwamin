from accounts.models import Profile
from chats.application import ChatApplication
from commons.patterns import Runnable
from dua_empat.application import DuaEmpatApplication
from .play import PlayService
from ..models import Play


class CommandService(Runnable):
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

        messages = None

        if is_play:
            if game_id == Play.Game.DUA_EMPAT:
                if text == 'udahan':
                    PlayService.end(source_id)
                    messages = DuaEmpatApplication.end(source_id)
                else:
                    messages = DuaEmpatApplication.reply(source_id, profile.id, text)
        else:
            if text == 'menu':
                messages = ['main 24']
            elif text.startswith('main'):
                if text == 'main 24':
                    PlayService.start(source_id, Play.Game.DUA_EMPAT)
                    DuaEmpatApplication.start(source_id)

        ChatApplication.reply(token, messages)
