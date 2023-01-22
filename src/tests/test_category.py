import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from src.teasers.models import Category

User = get_user_model()


@pytest.mark.django_db
def test_list_categories(api_client: APIClient) -> None:
    url = reverse('api:categories-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert Category.objects.count() == len(response.json())


@pytest.mark.django_db
def test_create_category(api_client: APIClient) -> None:
    url = reverse('api:categories-list')

    data = {
        'title': 'test-category-title',
        'description': 'test-category-description',
    }

    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert data['title'] == response.json()['title']


@pytest.mark.django_db
def test_update_category(api_client: APIClient) -> None:
    category = Category.objects.first()
    url = reverse('api:categories-detail', args=(category.pk,))

    data = {
        'title': 'test-category-title',
    }

    response = api_client.patch(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert data['title'] == response.json()['title']


@pytest.mark.django_db
def test_delete_teasers(api_client: APIClient) -> None:
    categories = Category.objects.all()
    category = categories.first()
    assert categories.count() == 1

    url = reverse('api:categories-detail', args=(category.pk,))
    response = api_client.delete(url)

    assert response.status_code == 204
    assert categories.count() == 0
