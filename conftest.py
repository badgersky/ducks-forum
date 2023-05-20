import pytest


@pytest.fixture
def user(db, django_user_model):
    """User instance"""

    user = django_user_model.create_user(
        username='username1',
        password='password1',
        )

    return user
