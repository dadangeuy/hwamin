from chat.client import ChatClient
from chat.models import Template, Carousel, Column, Postback
from chat.services import CreateMessageReplyService
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
                reply_texts = DuaEmpatClient.end(source_id)
                SessionClient.end_game(source_id)

        else:
            game = SessionClient.get_game(source_id)
            if game == 'dua_empat':
                reply_texts = DuaEmpatClient.reply(source_id, profile_id, text)
            else:
                cls._test_postback(token)

        ChatClient.send_text_reply(token, reply_texts)

    # TODO: remove
    @staticmethod
    def _test_postback(token: str) -> None:
        message = Template(
            alt_text='alt_text',
            template=Carousel(
                columns=[
                    Column(
                        text='column_1',
                        actions=[
                            Postback(
                                data='column_1_postback_1',
                                label='column_1_postback_1',
                            ),
                            Postback(
                                data='column_1_postback_2',
                                label='column_1_postback_2',
                            ),
                        ]
                    ),
                    Column(
                        text='column_2',
                        actions=[
                            Postback(
                                data='column_2_postback_1',
                                label='column_2_postback_1',
                            ),
                            Postback(
                                data='column_2_postback_2',
                                label='column_2_postback_1',
                            ),
                        ]
                    ),
                ]
            )
        )
        CreateMessageReplyService.run(token, [message])
