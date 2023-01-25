from django.db import  transaction
from rest_framework import serializers

from src.teasers.models import Teaser, PAID, REFUSAL
from src.teasers.services import UpdateTeaserStatusService
from src.wallets.models import Wallet
from src.wallets.services import UpdateWalletBalanceServices


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

    def create(self, validated_data) -> list[Teaser]:
        with transaction.atomic():
            teasers: list[Teaser] = UpdateTeaserStatusService(validated_data=validated_data)()
            UpdateWalletBalanceServices(teasers=teasers)()
        return teasers


class ResponseUpdateTeaserSerializer(serializers.Serializer):
    status = serializers.CharField(label='Статус', max_length=10)
