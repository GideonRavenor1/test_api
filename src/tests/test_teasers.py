import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from src.teasers.models import Teaser, Category
from src.wallets.models import Wallet

User = get_user_model()


@pytest.mark.django_db
def test_list_teasers(api_client: APIClient) -> None:
    url = reverse('api:teasers-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert Teaser.objects.count() == len(response.json())


@pytest.mark.django_db
def test_create_teasers(api_client: APIClient) -> None:
    url = reverse('api:teasers-list')
    user = User.objects.first()
    category = Category.objects.first()

    data = {
        'title': 'test-teaser-title',
        'description': 'test-teaser-description',
        'user': user.pk,
        'category': category.pk
    }

    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert data['title'] == response.json()['title']


@pytest.mark.django_db
def test_update_teasers(api_client: APIClient) -> None:
    teaser = Teaser.objects.first()
    url = reverse('api:teasers-detail', args=(teaser.pk,))

    data = {
        'title': 'test-teaser-title',
    }

    response = api_client.patch(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert data['title'] == response.json()['title']


@pytest.mark.django_db
def test_delete_teasers(api_client: APIClient) -> None:
    teasers = Teaser.objects.all()
    teaser = teasers.first()
    assert teasers.count() == 10

    url = reverse('api:teasers-detail', args=(teaser.pk,))
    response = api_client.delete(url)

    assert response.status_code == 204
    assert teasers.count() == 9


@pytest.mark.django_db
def test_change_statuses_with_author(api_client: APIClient) -> None:
    teasers = Teaser.objects.all()
    user = User.objects.select_related('wallet').first()
    url = reverse('api:teasers-status')

    data = {
        'teasers': [{'teaser_id': teaser.pk, 'status': teaser.STATUS.paid} for teaser in teasers]
    }

    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 403
    assert user.wallet.balance == 0


@pytest.mark.django_db
def test_change_statuses_with_admin(api_client: APIClient) -> None:
    teasers = Teaser.objects.all()

    admin = User.objects.create(username='fedor', password='test1993', role='admin')
    api_client.force_authenticate(user=admin)
    url = reverse('api:teasers-status')

    data = {
        'teasers': [{'teaser_id': teaser.pk, 'status': teaser.STATUS.paid} for teaser in teasers]
    }
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    balance = Wallet.available_objects.select_related('user').filter(user__username='someone').first().balance
    assert response.status_code == 200
    assert balance == 1000


@pytest.mark.django_db
def test_change_statuses_with_admin_if_payed(api_client: APIClient) -> None:
    teasers = Teaser.objects.all()
    teasers.update(status='paid')

    admin = User.objects.create(username='fedor', password='test1993', role='admin')
    api_client.force_authenticate(user=admin)
    url = reverse('api:teasers-status')

    data = {
        'teasers': [{'teaser_id': teaser.pk, 'status': teaser.STATUS.paid} for teaser in teasers]
    }
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')
    balance = Wallet.available_objects.select_related('user').filter(user__username='someone').first().balance
    assert response.status_code == 200
    assert balance == 0
