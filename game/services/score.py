from django.db import transaction
from django.db.models import F

from game.models import Score


class ScoreService:

    @classmethod
    def add_point(cls, source_id: str, profile_id: str, point: int) -> None:
        score_qs = Score.objects.filter(source_id=source_id, profile_id=profile_id)
        with transaction.atomic():
            updated_rows = score_qs.update(point=F('point') + point)
            if updated_rows == 0:
                Score.objects.create(source_id=source_id, profile_id=profile_id, point=point)

    @classmethod
    def get_info(cls, source_id: str) -> str:
        score_qs = Score.objects.filter(source_id=source_id).select_related('profile')
        score_lines = (f'{score.profile.name}: {score.point}' for score in score_qs.iterator())

        lines = ('[SCOREBOARD]', *score_lines,)
        info = '\n'.join(lines)

        return info

    @classmethod
    def clear(cls, source_id: str) -> None:
        score_qs = Score.objects.filter(source_id=source_id)
        score_qs.delete()
