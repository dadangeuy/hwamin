from django.db import transaction
from django.db.models import F

from common.patterns import Runnable
from session.models import Score


class UpdateScoreService(Runnable):

    @classmethod
    def run(cls, source_id: str, profile_id: str, point: int) -> None:
        score_qs = Score.objects.filter(source_id=source_id, profile_id=profile_id)
        with transaction.atomic():
            updated_rows = score_qs.update(point=F('point') + point)
            if updated_rows == 0:
                Score.objects.create(source_id=source_id, profile_id=profile_id, point=point)
