from chat.client import ChatClient
from dua_empat.client import DuaEmpatClient
from session.client import SessionClient


class CommandClient:

    @classmethod
    def run_command(cls, token: str, source_id: str, profile_id: str, text: str) -> None:
        command = text.lower()
        reply_texts = None

        if command.startswith('main'):
            if command == 'main 24':
                SessionClient.start_game(source_id, 'dua_empat')
                reply_texts = DuaEmpatClient.start(source_id)

        elif command == 'udahan':
            game = SessionClient.get_game(source_id)
            if game == 'dua_empat':
                SessionClient.end_game(source_id)
                reply_texts = DuaEmpatClient.end(source_id)

        else:
            game = SessionClient.get_game(source_id)
            if game == 'dua_empat':
                reply_texts = DuaEmpatClient.reply(source_id, profile_id, text)

        ChatClient.send_text_reply(token, reply_texts)
