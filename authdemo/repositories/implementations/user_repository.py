from authdemo.repositories.interfaces.user_repository_interface import UserRepositoryInterface
from django.db.utils import OperationalError
from authdemo.models import User
from django.db.utils import IntegrityError
from authdemo.repositories.mixins import ModelCrudMixin
import logging

logger = logging.getLogger(__name__)


class UserRepository(UserRepositoryInterface, ModelCrudMixin):
    @classmethod
    def create_user(cls, data: dict) -> User:
        logger.info(f'Creating new user with {data=}')
        if not data:
            logger.info('Attempt to create a new User without data, exiting')
            raise ValueError("Data is empty")
        if not isinstance(data, dict):
            logger.error(f"Trying to create a User with inconsistent data")
            raise ValueError("Data should be dict-like")
        if data.get("user_id"):
            logger.warning(f"Attempt to create a new user with pkey: user_id = {data['user_id']}, this will be ignored")
            data.pop("user_id", False)
        return cls.create_model(User, data)

    @classmethod
    def get_or_create_user(cls, data: dict) -> tuple[User, bool]:
        """
        Get or create a user instance based on the provided data.

        Args:
            data (dict): Data containing fields for creating or identifying the user.

        Returns:
            tuple[User, bool]: The user instance and a boolean indicating if it was created.

        Raises:
            OperationalError: If there is a database error.
        """
        try:
            user, created = User.objects.get_or_create(
                email=data.get('email'),
                defaults=data
            )
            return user, created
        except OperationalError as e:
            raise OperationalError(f"Database error has occurred: {str(e)}")
        # try:
        #     all_field_names = {field.name for field in User._meta.get_fields()}
        #     unique_field_names = {
        #         field.name for field in User._meta.get_fields() if getattr(field, 'unique', False)
        #     }
        #     non_unique_fields = all_field_names - unique_field_names
        #
        #     # Extract unique fields and their values from the data dictionary
        #     identifiers = {key: data[key] for key in unique_field_names if key in data}
        #     print(identifiers)
        #     defaults = {key: data[key] for key in non_unique_fields if key in data}
        #     print(defaults)
        #     user, created = User.objects.get_or_create(**identifiers, defaults=defaults)
        #     return user, created
        # except OperationalError as e:
        #     raise OperationalError(f"Database error has occurred : {str(e)}")

    def get_user(self, user_id: int):
        pass

    def delete_user(self, user_id: int):
        pass
