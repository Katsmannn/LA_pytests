import pytest

from api.models import UserRole


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567')


@pytest.fixture
def user_admin_teacher_role(user, role_admin, role_teacher):
    UserRole.objects.create(user=user, role=role_admin)
    UserRole.objects.create(user=user, role=role_teacher)
