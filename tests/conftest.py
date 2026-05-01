import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def default_customer():
    User = get_user_model()
    return User.objects.create_user(
        username="default_customer",
        email="default@example.com",
        first_name="Default",
        last_name="Customer",
    )
