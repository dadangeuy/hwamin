from typing import Optional

from game.models import Play


class PlayService:
    @classmethod
    def start(cls, source_id: str, game_id: str) -> None:
        Play.objects.create(source_id=source_id, game_id=game_id)

    @classmethod
    def end(cls, source_id: str) -> None:
        Play.objects.filter(source_id=source_id).delete()

    @classmethod
    def get_game_id(cls, source_id: str) -> Optional[str]:
        play_qs = Play.objects.filter(source_id=source_id).only('game_id')
        game_id = play_qs.first().game_id if play_qs.exists() else None

        return game_id
