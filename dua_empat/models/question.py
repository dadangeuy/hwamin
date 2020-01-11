from uuid import uuid4

from django.db.models import Model, IntegerField, UUIDField, CharField, UniqueConstraint


class Question(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    first_number = IntegerField(default=0)
    second_number = IntegerField(default=0)
    third_number = IntegerField(default=0)
    fourth_number = IntegerField(default=0)
    source_id = CharField(max_length=33, editable=False)

    class Meta:
        db_table = 'question'
        constraints = [
            UniqueConstraint(
                fields=['source_id'],
                name='question_has_unique_source_id'
            )
        ]

    @property
    def display_numbers(self) -> str:
        return self.numbers.__str__()

    @property
    def numbers(self) -> (int, int, int, int):
        return self.first_number, self.second_number, self.third_number, self.fourth_number
