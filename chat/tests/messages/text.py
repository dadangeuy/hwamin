from chat.models import Text


class TestText:
    def test_dumps(self):
        message = Text(text='Hello, World!')
        json_str = message.to_json()
        assert json_str == '{"text": "Hello, World!", "type": "text"}'
