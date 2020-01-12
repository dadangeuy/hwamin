from typing import List

from chat.services import CreateTextReplyService


class ChatApplication:

    @classmethod
    def send_text_reply(cls, token: str, text_messages: List[str]) -> None:
        CreateTextReplyService.run(token, text_messages)
