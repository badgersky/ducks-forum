from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.models import Thread, Comment


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


@pytest.fixture
def comment(db, client, user, thread):
    """comment instance"""

    client.force_login(user)

    comment = Comment.objects.create(
        thread=thread,
        user=user,
        content='comment content',
    )

    return comment


@pytest.fixture
def image():
    """temporary image object"""

    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())
