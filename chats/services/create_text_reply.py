from commons.patterns import Runnable
from .create_reply import CreateReplyService


class CreateTextReplyService(Runnable):

    @classmethod
    def run(cls, token: str, texts: list, notification: bool = True) -> None:
        if texts is None or len(texts) == 0:
            return

        messages = [{'type': 'text', 'text': text} for text in texts]
        data = {
            'replyToken': token,
            'messages': messages,
            'notificationDisabled': not notification
        }
        CreateReplyService.run(data)
