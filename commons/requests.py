from requests import Session


class PublicApiSession(Session):
    def __init__(self):
        super().__init__()
        self.headers['Content-Type'] = 'application/json'
