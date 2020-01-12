from typing import Optional

from session.models import Play


class PlayService:
    @classmethod
    def start_game(cls, source_id: str, game_id: str) -> None:
        Play.objects.create(source_id=source_id, game_id=game_id)

    @classmethod
    def end_game(cls, source_id: str) -> None:
        Play.objects.filter(source_id=source_id).delete()

    @classmethod
    def get_game(cls, source_id: str) -> Optional[Play.Game]:
        play = Play.objects.filter(source_id=source_id).only('game_id').first()
        return play.game_id if play else None
