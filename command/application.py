from chat import ChatApplication
from dua_empat import DuaEmpatApplication
from session import SessionApplication


class CommandApplication:

    @classmethod
    def run_command(cls, token: str, source_id: str, profile_id: str, text: str) -> None:
        command = text.lower()
        reply_texts = None

        if command.startswith('main'):
            if command == 'main 24':
                SessionApplication.start_game(source_id, 'dua_empat')
                reply_texts = DuaEmpatApplication.start(source_id)

        elif command == 'udahan':
            game = SessionApplication.get_game(source_id)
            if game == 'dua_empat':
                SessionApplication.end_game(source_id)
                reply_texts = DuaEmpatApplication.end(source_id)

        else:
            game = SessionApplication.get_game(source_id)
            if game == 'dua_empat':
                reply_texts = DuaEmpatApplication.reply(source_id, profile_id, text)

        ChatApplication.send_text_reply(token, reply_texts)
