from session.services import PlayService, ScoreService


class SessionApplication:

    @staticmethod
    def start_game(source_id: str, game_id: str) -> None:
        PlayService.start_game(source_id, game_id)

    @staticmethod
    def end_game(source_id: str) -> None:
        PlayService.end_game(source_id)
        ScoreService.clear(source_id)

    @staticmethod
    def get_game(source_id: str) -> str:
        return PlayService.get_game(source_id)

    @staticmethod
    def get_score_info(source_id: str) -> str:
        return ScoreService.get_info(source_id)

    @staticmethod
    def update_score_point(source_id: str, profile_id: str, point: int) -> None:
        ScoreService.add_point(source_id, profile_id, point)
