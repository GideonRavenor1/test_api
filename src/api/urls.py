from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.api.swagger.urls import urlpatterns as swagger_urls
from src.api.views import TeaserModelViewSet, CategoryModelViewSet

app_name = 'api'

router = DefaultRouter()
router.register('teasers', TeaserModelViewSet, basename='teasers')
router.register('categories', CategoryModelViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += swagger_urls
