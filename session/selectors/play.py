from typing import Optional

from session.models import Play


class PlaySelector:

    @classmethod
    def get_game(cls, source_id: str) -> Optional[Play.Game]:
        play = Play.objects.filter(source_id=source_id).only('game_id').first()
        return play.game_id if play else None
