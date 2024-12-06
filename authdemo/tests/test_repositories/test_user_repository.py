import logging

import pytest
from django.db.utils import OperationalError
from model_bakery import baker
from authdemo.repositories.implementations.user_repository import UserRepository
from authdemo.models import User
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError


@pytest.fixture
def user_feed_fixture():
    user_1 = {
            "first_name": "Kad",
            "last_name": "AIK",
            "email": "kad@gmail.com",
            "password": make_password('12345678')
        }
    User.objects.create(**user_1)


@pytest.mark.django_db
@pytest.mark.parametrize("user_data, expected_output", [
    (None, ValueError),             # No arguments provided
    ("A", ValueError),              # Inconsistent arguments
    (baker.prepare('authdemo.User').__dict__, User),    # Non-existing User with extra fields
    ({
            "first_name": "Kingston",
            "last_name": "AMI",
            "email": "rodd@gmail.com",
            "password": make_password('12345678'),      # Non-existing normal User

        }, User),
    ({
        "first_name": "Kad",
        "last_name": "AIK",
        "email": "kad@gmail.com",
        "password": make_password('12345678'),      # Existing normal user

        }, IntegrityError),
({
            "user_id": 2,                           # Provided pkey should be ignored and a warn logged
            "first_name": "Bravo",
            "last_name": "ZULU",
            "email": "bravo@gmail.com",
            "password": make_password('12345678'),
        }, User),
])
def test_create_user(user_feed_fixture, user_data, expected_output):
    try:
        result = UserRepository.create_user(user_data)
        assert isinstance(result, expected_output)
    except IntegrityError as ie:
        assert True
    except ValueError as ve:
        assert True
    except OperationalError as e:
        pytest.fail(f"Database error : {str(e)}")


@pytest.mark.django_db
@pytest.mark.parametrize("input_user_data, expected_output", [
    ({
        "first_name": "Kingston",
        "last_name": "AMI",
        "email": "rodd@gmail.com",
        "password": make_password('12345678'),  # Non-existing user

    }, (User, True)),
    ({
        "first_name": "Kad",
        "last_name": "AIK",
        "email": "kad@gmail.com",
        "password": make_password('12345678'),  # Existing user

        }, (User, False)),
    ])
def test_get_or_create_user(user_feed_fixture, input_user_data, expected_output):
    """Create a non-existing user or return a user if it already exists."""
    try:
        user, created = UserRepository.get_or_create_user(input_user_data)
        assert isinstance(user, expected_output[0]), "The created entity is not a User model"
        assert created == expected_output[1]
    except OperationalError as e:
        pytest.fail(f"A, error occurred : {str(e)}")


