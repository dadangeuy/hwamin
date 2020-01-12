from common.patterns import Runnable
from session.models import Play


class CreatePlayService(Runnable):

    @classmethod
    def run(cls, source_id: str, game_id: str) -> None:
        Play.objects.create(source_id=source_id, game_id=game_id)
