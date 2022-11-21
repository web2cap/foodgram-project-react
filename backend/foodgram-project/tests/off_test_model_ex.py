import pytest
from users.models import User
from django.test import override_settings


@pytest.mark.skip(reason='Not ready for testing. TODO: timezone varnings')
@pytest.mark.django_db
def test_user_create():
    with override_settings(USE_TZ=False):
        User.objects.create_user('user', 'user@mail.com', 'password')
    assert User.objects.count() == 1