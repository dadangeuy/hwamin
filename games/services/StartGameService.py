from django.contrib.sessions.backends.base import SessionBase

from chats.services import CreateReplyService
from commons.patterns import Runnable
from games.services import DuaEmpatGeneratorService


class StartGameService(Runnable):
    @classmethod
    def run(cls, session: SessionBase, token: str, text: str) -> None:
        messages = []

        if text == 'main 24':
            session['question'] = DuaEmpatGeneratorService.run()
            session['game'] = 'DUA_EMPAT'
            session['scoreboard'] = {}
            messages.append('game dimulai')
            messages.append(session['question'].__str__())

        CreateReplyService.run(token, messages)
