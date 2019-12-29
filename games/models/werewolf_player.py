from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, TextChoices, UniqueConstraint
from django.utils.translation import gettext_lazy


class WerewolfPlayer(Model):
    class Role(TextChoices):
        VILLAGER = 'v', gettext_lazy('Penduduk')
        WEREWOLF = 'w', gettext_lazy('Werewolf')
        SEER = 's', gettext_lazy('Peramal')
        DOCTOR = 'd', gettext_lazy('Dokter')

    source_id = CharField(max_length=33, editable=False)
    profile = ForeignKey(to='accounts.profile', on_delete=CASCADE)
    is_alive = BooleanField(default=True)
    role = CharField(max_length=1, choices=Role.choices, default=Role.VILLAGER)

    class Meta:
        db_table = 'werewolf_player'
        constraints = [
            UniqueConstraint(fields=['source_id', 'profile'], name='werewolf_player_has_unique_source_id_profile')
        ]
