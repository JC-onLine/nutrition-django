import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

pytestmark = pytest.mark.django_db # remplace le décorateur @pytest.mark.django_db

User = get_user_model()


def test_create_user():
    """
    Given valid user data
    When creating user
    Then user should be created with correct attributes and not be staff or superuser
    """
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="motdepasse123456"
    )

    assert user.username == "testuser"
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser():
    """
    Given valid user data
    When creating superuser
    Then user should be created with correct attributes be staff and superuser
    """
    user = User.objects.create_superuser(
        username="adminuser",
        email="test2@example.com",
        password="motdepasse1234567"
    )

    assert user.username == "adminuser"
    assert user.is_staff
    assert user.is_superuser


def test_create_user_without_username():
    """
    Given user data without username
    When creating user
    Then it should raise a ValueError
    """
    with pytest.raises(ValueError, match="Le nom est obligatoire"):
        User.objects.create_user(
            username="",
            email="t@t.com",
            password="motdepasse123456"
        )


def test_email_unique(user1): # user1 est créé dans la fixture user1 (fonction) de conftest.py
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="user2",
            email="test@example.com",
            password="motdepasse123456"
        )
