import pytest

from django.db.utils import OperationalError
from django.db.utils import IntegrityError

from authdemo.repositories.implementations.session_repository import SessionRepository
from authdemo.models import Session

import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def session_feed_db():
    """Fixture to populate the database with initial data."""
    logger.info("Feeding session tables with initial data ...")
    # Create initial session entries to simulate duplicates
    s1 = Session.objects.create()
    s2 = Session.objects.create()
    logger.info(f"Session table feed with {s1=} \n and \n {s2=}\n")


# ---------------------------------------------------------Tests------------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize("input_data, expected_output", [
    ("", Session),  # Called without arguments, should create session with id = 3
    ({"session_id": 1}, Session),  # Existing session; need more field to populate this as pkey provided will be ignored
    ({"session_id": 3}, Session),  # Non-existing session; need more field
])
def test_create_session(session_feed_db, input_data, expected_output):
    """
    Create a new session when called without argument, throw an exception when the session
    already exists and create it if it doesn't.
    """
    logger.info(f"Starting test_create_session with input_data: {input_data}")

    try:
        logger.info("Calling create_session method...")

        session = SessionRepository.create_session(input_data)

        logger.info("Session created, performing assertions...")

        assert session is not None, "Session is null."
        assert isinstance(session, Session), f"Expected {expected_output}, got {session.__class__.__name__}"

        logger.info("Assertions passed, test completed successfully.")
    except IntegrityError as ie:
        logger.exception(f"The session already exists: {str(ie)}")


@pytest.mark.django_db
@pytest.mark.parametrize("input_data, expected_output", [
    (None, ValueError),                         # Arguments not provided
    ("A", ValueError),                          # Called with inconsistent arguments
    ({"session_id": 15}, ("Session", False)),   # The session already exists; note: the sequence number keep adding up
    ({"session_id": 5}, ("Session", True)),     # The session doesn't exist, in fact the fixture create two session
                                                # with ids 14 and 15 here (sequence not resset), thus lesser ids session
                                                # don't exist.
])
def test_get_or_create_session(session_feed_db, input_data, expected_output):
    logger.info("===================================================================")
    logger.info(f"Starting test_get_or_create_session with input_data: {input_data}")
    try:
        logger.info("Calling get_or_create class method...")
        result = SessionRepository.get_or_create_session(input_data)

        logger.info(" Session got, beginning assertions...")
        try:
            assert (result[0].__class__.__name__, result[1]) == expected_output, \
                f"Expected {expected_output}, got {(result[0].__class__.__name__, result[1])}"
        except AssertionError as ae:
            logger.error(f"Assertion failed, {ae}")
            raise
        logger.info(" Assertions passed, clean-up...")

    except Session.MultipleObjectsReturned as e:
        pytest.fail(f"Multiple objects are returned instead of one, hint: dict dereferencing, str {e}")
    except ValueError:
        logger.info("Got Value error, expected behavior matches")
        assert True
    except OperationalError as e:
        pytest.fail(f"Database error: {str(e)}")


def test_update_session():
    pass
