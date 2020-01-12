from session.selectors import PlaySelector, ScoreSelector
from session.services import DeleteScoreService, UpdateScoreService, CreatePlayService, DeletePlayService


class SessionApplication:

    @staticmethod
    def start_game(source_id: str, game_id: str) -> None:
        CreatePlayService.run(source_id, game_id)

    @staticmethod
    def end_game(source_id: str) -> None:
        DeletePlayService.run(source_id)
        DeleteScoreService.run(source_id)

    @staticmethod
    def get_game(source_id: str) -> str:
        return PlaySelector.get_game(source_id)

    @staticmethod
    def get_score_board(source_id: str) -> str:
        return ScoreSelector.get_score_board(source_id)

    @staticmethod
    def update_score(source_id: str, profile_id: str, point: int) -> None:
        UpdateScoreService.run(source_id, profile_id, point)
