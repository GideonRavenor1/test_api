import uuid

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from src.teasers.models import Category, Teaser
from src.wallets.models import Wallet

User = get_user_model()


@pytest.fixture
def create_user(db, django_user_model) -> User:
    data = {
        'username': 'someone',
        'password': 'some_password'
    }
    user: User = django_user_model.objects.create_user(**data)
    user.refresh_from_db()
    wallet: Wallet = user.wallet
    wallet.fixed_price = 100
    wallet.save(update_fields=['fixed_price'])
    return user


@pytest.fixture
def create_category(db) -> Category:
    data = {
        'title': 'some_title',
        'description': 'some_description'
    }
    return Category.objects.create(**data)


@pytest.fixture
def initial_data(db, create_user: User, create_category: Category) -> User:
    user = create_user
    category = create_category
    teasers = [
        Teaser(
            title=uuid.uuid4().hex,
            description='some_description',
            user=user,
            category=category
        ) for _ in range(10)
    ]
    Teaser.objects.bulk_create(teasers)
    return user


@pytest.fixture
def api_client(initial_data: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=initial_data)
    return client
