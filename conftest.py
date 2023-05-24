import pytest

from forum.models import Thread


@pytest.fixture
def user(db, django_user_model):
    """User instance"""

    user = django_user_model.objects.create_user(
        username='username1',
        password='password1',
        )

    return user


@pytest.fixture
def thread(db, client, user):
    """Thread instance"""

    client.force_login(user)

    thread = Thread.objects.create(
        subject='subject1',
        content='content1',
        creator=user,
    )

    return thread
