import pytest
from pytest_mock import MockFixture
from requests import Response

from chat.models import Text, Template, Carousel
from chat.services import CreateMessageReplyService as service


class TestCreateMessageReplyService:

    @pytest.fixture(autouse=True)
    def setup_mock(self, mocker: MockFixture):
        response = Response()
        response.status_code = 200
        mocker.patch(f'{service.__module__}.post', return_value=response)

    def test_run(self):
        service.run(
            token='qwerty',
            messages=[
                Text(text='Hello, World!'),
                Template(
                    alt_text='Menu',
                    template=Carousel(
                        columns=[]
                    )
                ),
            ],
            notification=False
        )
