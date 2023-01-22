from rest_framework import serializers

from src.teasers.models import Teaser, PAID, REFUSAL
from src.wallets.models import Wallet


class TeaserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teaser
        fields = ('id', 'category', 'user', 'title', 'description', 'status', 'created', 'modified')
        read_only_fields = ('status', 'user', 'created', 'modified')

    def create(self, validated_data: dict) -> Teaser:
        request = self.context['request']
        return self.Meta.model.objects.create(user=request.user, **validated_data)

    def validate_title(self, value: str) -> str:
        request = self.context['request']
        if self.Meta.model.objects.filter(user=request.user, title=value).exists():
            raise serializers.ValidationError('Тизер должен быть уникальным')
        return value


class UpdateTeaserSerializer(serializers.Serializer):
    teaser_id = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=[PAID, REFUSAL])


class SetTeaserStatusSerializer(serializers.Serializer):
    teasers = UpdateTeaserSerializer(many=True)

    def update_statuses(self) -> list[Teaser]:
        teasers_dict = {element['teaser_id']: element['status'] for element in self.validated_data['teasers']}
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

        Teaser.objects.bulk_update(teasers, fields=['status'])
        return teasers

    def pay_for_work(self, teasers: list[Teaser]) -> None:
        wallets = []
        for teaser in teasers:
            if teaser.status != teaser.STATUS.paid:
                continue
            wallet: Wallet = teaser.user.wallet
            wallet.transfer_amount()
            wallets.append(wallet)

        Wallet.objects.bulk_update(wallets, fields=['balance'])


class ResponseUpdateTeaserSerializer(serializers.Serializer):
    status = serializers.CharField(label='Статус', max_length=10)
