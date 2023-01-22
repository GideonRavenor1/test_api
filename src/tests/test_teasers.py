import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from src.teasers.models import Teaser

User = get_user_model()


@pytest.mark.django_db
def test_unauthorized_request(api_client: APIClient):
    url = reverse('api:teasers-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert Teaser.objects.count() == 10
