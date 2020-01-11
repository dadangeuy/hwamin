from typing import List

from chats.services import CreateTextReplyService


class ChatApplication:

    @classmethod
    def reply(cls, token: str, messages: List[str]) -> None:
        CreateTextReplyService.run(token, messages)
