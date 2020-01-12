from common.patterns import Runnable
from session.models import Play


class DeletePlayService(Runnable):

    @classmethod
    def run(cls, source_id: str) -> None:
        Play.objects.filter(source_id=source_id).delete()
