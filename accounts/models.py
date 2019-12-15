from uuid import uuid4

from django.db.models import UUIDField, CharField, Model
from django.db.models.constraints import UniqueConstraint


class LineAccount(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    line_id = CharField(max_length=33, editable=False)

    class Meta:
        db_table = 'line_account'
        constraints = [
            UniqueConstraint(fields=['line_id'], name='line_account_has_unique_line_id')
        ]
