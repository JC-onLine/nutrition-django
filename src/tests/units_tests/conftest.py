import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user1(): # user1 est un fixture qui peut s'appuyer sur d'autres fixtures'
    return  User.objects.create_user(username="user1",
                                     email="test@example.com",
                                     password="motdepasse123456")
