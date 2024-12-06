from authdemo.repositories.interfaces.session_repository_interface import SessionRepositoryInterface

from authdemo.models import Session

from django.db.utils import OperationalError
from django.db.utils import IntegrityError
from authdemo.repositories.mixins import ModelCrudMixin

import logging

logger = logging.getLogger(__name__)


class SessionRepository(SessionRepositoryInterface, ModelCrudMixin):
    @classmethod
    def create_session(cls, data: dict) -> Session:
        """
        Creates a new `Session` object based on the provided data attributes or raises an error
        if the session already exists.

        The `session_id` primary key, if provided in the input `data`, is ignored to ensure
        database consistency and to avoid unique constraint violations. If `data` is empty,
        an empty `Session` object is created.

        Args:
            data (dict): A dictionary containing the attributes for the new `Session` object.
                If `session_id` is included, it will be removed before the session creation.

        Returns:
            Session: The created `Session` object.

        Raises:
            IntegrityError: If a session with the same unique constraints already exists.

        Logging:
            - Logs entry into the method and the received data.
            - Logs removal of the `session_id` field if present in `data`.
            - Logs success or failure during the session creation process.

        Notes:
            - This method calls `create_model` from `ModelCrudMixin` to handle model creation.
            - Handles potential errors during the creation process and logs them.

        Example:
            ```python
            session_data = {"user_id": 123, "status": "active"}
            new_session = SessionRepository.create_session(session_data)
            ```
        """
        logger.info(f"Entered create_session method with data: {data}")
        logger.info(f"Data received in create_session: {data}")

        if not data:
            logger.info(f"The conditional block is executing assuming data is None")
            try:
                session = Session.objects.create()
                logger.info(f"Successfully created Session with ID: {session.session_id}")
                return session
            except IntegrityError as e:
                logger.error(f"IntegrityError occurred: {e}")
                raise

        # To ensure consistency and avoid sequence updating issues at the DB level,
        # which may lead to unique constraint violations on the primary key,
        # a primary key (`session_id`) if provided is always ignored as it is an auto-increment field.
        if data.get("session_id"):
            logger.info("data contains a user manually defined pkey auto increment field session_id; field removed")
            del data["session_id"]

        logger.info('Calling mixin create_model method...')
        return cls.create_model(Session, data)

    @classmethod
    def get_or_create_session(cls, data: dict) -> Session:
        """
        Get the corresponding session (based on its id) or create a new one and return it.

        Returns: tuple
             A tuple containing the created Session or the fetched one and a boolean
             indicating if the session is created or not.
        """
        logger.info(f"Entered get_or_create_session with {data=}")
        if not data:
            logger.exception("data is empty (evaluate to False, exiting...")
            raise ValueError("Session attributes not provided")

        if not isinstance(data, dict):
            logger.exception("data is not a dict-like, exiting...")
            raise ValueError("Data should be a dict like")

        if not data.get('session_id'):
            logger.exception("missing session_id key in data, exiting...")
            raise KeyError('session identifier (session_id) field not provided')
        try:
            logger.info(f"Got {data['session_id']=}")
            logger.info("Fetching the session object...")
            session = Session.objects.get(session_id=data['session_id'])
            logger.info("Object exists and is fetched, returning...")
            return session, False
        except Session.DoesNotExist:
            logger.exception(f"Model with {data['session_id']=} doesn't exist, creating a new session object...")
            data.pop('session_id', None)
            try:
                logger.info(f"Creating a new session with {data}")
                session = Session.objects.create(**data)
                logger.info(f"New session created with {session.session_id=} returning...")
                return session, True
            except OperationalError as oe:
                logger.error("A database error occurred when fetching or creating a new session, exiting...")
                raise OperationalError(f"Database error : {str(oe)}")

    def get_session(self, session_id: int):
        pass

    def delete_session(self, session_id: int):
        pass
