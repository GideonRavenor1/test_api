from src.bases.services import BaseServices
from src.teasers.models import Teaser


class UpdateTeaserStatusService(BaseServices):

    def __init__(self, validated_data: dict) -> None:
        self.data = validated_data

    def __call__(self) -> list[Teaser]:
        teasers_dict = {element['teaser_id']: element['status'] for element in self.data['teasers']}
        found_teasers = (
            Teaser.objects.select_related('user')
            .prefetch_related('user__wallet')
            .filter(id__in=teasers_dict.keys())
        )

        teasers = []
        for teaser in found_teasers:

            if teaser.pk not in teasers_dict:
                continue

            if teaser.status != teaser.STATUS.undefined:
                continue

            teaser.status = teasers_dict[teaser.pk]
            teasers.append(teaser)

        Teaser.objects.select_for_update().bulk_update(teasers, fields=['status'])
        return teasers
