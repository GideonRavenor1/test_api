from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

User = get_user_model()


class UserSerializer(DjoserUserSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role')
        read_only_fields = ('role',)


class CurrentUserSerializer(DjoserUserSerializer):
    fixed_price = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'fixed_price', 'balance')
        read_only_fields = ('role',)

    @swagger_serializer_method(serializer_or_field=serializers.FloatField)
    def get_fixed_price(self, obj: User) -> float:
        user = self.context['request'].user
        try:
            fixed_price = user.wallet.fixed_price
        except ObjectDoesNotExist:
            fixed_price = 0
        return fixed_price

    @swagger_serializer_method(serializer_or_field=serializers.FloatField)
    def get_balance(self, obj: User) -> float:
        user = self.context['request'].user
        try:
            balance = user.wallet.balance
        except ObjectDoesNotExist:
            balance = 0
        return balance
