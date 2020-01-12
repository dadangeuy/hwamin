from session.services import PlayService


class SessionApplication:

    @staticmethod
    def start_game(source_id: str, game_id: str) -> None:
        PlayService.start_game(source_id, game_id)

    @staticmethod
    def end_game(source_id: str) -> None:
        PlayService.end_game(source_id)

    @staticmethod
    def get_game(source_id: str) -> str:
        return PlayService.get_game(source_id)
