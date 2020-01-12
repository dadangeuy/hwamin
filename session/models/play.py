from uuid import uuid4

from django.db.models import Model, TextChoices, CharField, UniqueConstraint, UUIDField


class Play(Model):
    class Game(TextChoices):
        DUA_EMPAT = 'dua_empat'

    id = UUIDField(primary_key=True, default=uuid4)
    source_id = CharField(max_length=33, editable=False)
    game_id = CharField(max_length=16, choices=Game.choices)

    class Meta:
        db_table = 'play'
        constraints = [
            UniqueConstraint(
                fields=['source_id'],
                name='play_has_unique_source_id'
            )
        ]
