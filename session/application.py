from session.services import PlayService, DeleteScoreService, UpdateScoreService, GetScoreBoardService


class SessionApplication:

    @staticmethod
    def start_game(source_id: str, game_id: str) -> None:
        PlayService.start_game(source_id, game_id)

    @staticmethod
    def end_game(source_id: str) -> None:
        PlayService.end_game(source_id)
        DeleteScoreService.run(source_id)

    @staticmethod
    def get_game(source_id: str) -> str:
        return PlayService.get_game(source_id)

    @staticmethod
    def get_score_board(source_id: str) -> str:
        return GetScoreBoardService.run(source_id)

    @staticmethod
    def update_score(source_id: str, profile_id: str, point: int) -> None:
        UpdateScoreService.run(source_id, profile_id, point)
