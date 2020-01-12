from common.patterns import Runnable
from session.models import Score


class GetScoreBoardService(Runnable):

    @classmethod
    def run(cls, source_id: str) -> str:
        score_qs = Score.objects.filter(source_id=source_id).select_related('profile').order_by('-point')
        score_lines = (f'{score.profile.name}: {score.point}' for score in score_qs.iterator())

        lines = ('[SCOREBOARD]', *score_lines,)
        score_board = '\n'.join(lines)

        return score_board
