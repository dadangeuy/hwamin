from common.patterns import Runnable
from session.models import Score


class DeleteScoreService(Runnable):

    @classmethod
    def run(cls, source_id: str) -> None:
        score_qs = Score.objects.filter(source_id=source_id)
        score_qs.delete()
