from games.services import CommandService


class GameApplication:

    @classmethod
    def run_command(cls, source_id: str, profile_id: str, text: str, token: str):
        CommandService.run(token, text, source_id, profile_id)
