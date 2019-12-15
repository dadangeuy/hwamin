from typing import List

from django.db.transaction import atomic

from accounts.models import LineAccount
from commons.patterns import Runnable


class BulkCreateLineAccountService(Runnable):
    @classmethod
    @atomic(savepoint=False)
    def run(cls, line_ids: List[str]) -> List[LineAccount]:
        return [
            LineAccount.objects.get_or_create(line_id=line_id)
            for line_id in line_ids
        ]
