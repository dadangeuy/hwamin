from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Profile
from commons.patterns import Runnable
from externals.services import RetrieveProfileLineService


class RetrieveProfileService(Runnable):
    @classmethod
    def run(cls, profile_id: str) -> Profile:
        try:
            return Profile.objects.get(id=profile_id)
        except ObjectDoesNotExist:
            profile = RetrieveProfileLineService.run(profile_id)
            profile.save()
            return profile
