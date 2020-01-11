from uuid import uuid4

from django.db.models import Model, UUIDField, ForeignKey, CASCADE, CharField, IntegerField, UniqueConstraint


class Score(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    source_id = CharField(max_length=33, editable=False)
    profile = ForeignKey(to='account.Profile', editable=False, on_delete=CASCADE)
    point = IntegerField(default=0)

    class Meta:
        db_table = 'score'
        constraints = [
            UniqueConstraint(
                fields=['source_id', 'profile'],
                name='score_has_unique_source_id_and_profile'
            )
        ]
