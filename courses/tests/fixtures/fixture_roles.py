from django.db import models
import pytest


class TestRole(models.TextChoices):
    MAIN_ADMIN = 'MAdmin', 'Main administrator'
    ADMIN = 'Admin', 'Administrator'
    TEACHER = 'Teacher', 'Teacher'
    VOLUNTEER = 'Volunteer', 'Volunteer'


@pytest.fixture
def role_admin():
    return TestRole.ADMIN


@pytest.fixture
def role_main_admin():
    return TestRole.MAIN_ADMIN


@pytest.fixture
def role_teacher():
    return TestRole.TEACHER


@pytest.fixture
def role_volunteer():
    return TestRole.VOLUNTEER
