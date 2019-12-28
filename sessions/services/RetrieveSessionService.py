from collections import defaultdict

from requests import Session

from commons.patterns import Runnable
from commons.requests import PublicApiSession


class RetrieveSessionService(Runnable):
    SESSION_BY_SOURCE_ID = defaultdict(PublicApiSession)

    @classmethod
    def run(cls, source_id: str) -> Session:
        session = cls.SESSION_BY_SOURCE_ID[source_id]
        return session