from typing import Type

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.api.permissions import IsAuthorOrReadOnly, IsAdminUser
from src.api.serializers.categories import CategoriesSerializer
from src.api.serializers.teasers import TeaserSerializer, SetTeaserStatusSerializer, ResponseUpdateTeaserSerializer
from src.teasers.models import Teaser, Category


@method_decorator(
    name='status',
    decorator=swagger_auto_schema(
        request_body=SetTeaserStatusSerializer(),
        responses={status.HTTP_200_OK: ResponseUpdateTeaserSerializer()},
    ),
)
class TeaserModelViewSet(ModelViewSet):
    queryset = Teaser.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    swagger_tags = ('teasers',)

    def get_serializer_class(self) -> Type[SetTeaserStatusSerializer | TeaserSerializer]:
        if self.action == 'status':
            return SetTeaserStatusSerializer
        return TeaserSerializer

    @action(detail=False, methods=['POST'], permission_classes=[IsAdminUser])
    def status(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teasers = serializer.update_statuses()
        serializer.pay_for_work(teasers=teasers)
        return Response(status=status.HTTP_200_OK, data={'status': 'Успешно'})


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    swagger_tags = ('category',)
