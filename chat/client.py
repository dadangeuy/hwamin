from typing import List

from chat.services import CreateTextReplyService


class ChatClient:

    @staticmethod
    def send_text_reply(token: str, text_messages: List[str]) -> None:
        CreateTextReplyService.run(token, text_messages)
