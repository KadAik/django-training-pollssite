from django.db.utils import IntegrityError
from django.db.utils import OperationalError
from psycopg.errors import UniqueViolation
import logging

logger = logging.getLogger(__name__)


class ModelCrudMixin:
    @classmethod
    def create_model(cls, model, data):
        """
        Creates an instance of the specified Django model with the provided data.

        This method validates the input data against the model's fields, filters out any invalid fields,
        and attempts to create a new instance of the model. Logs and handles potential errors during the
        creation process.

        Args:
            model (Model): The Django model class to create an instance of.
            data (dict): A dictionary containing the data for the new model instance.

        Returns:
            Model: The newly created model instance.

        Raises:
            IntegrityError: If an instance with the same unique field already exists.
            OperationalError: If a database operational error occurs.
            Exception: If any other unexpected error occurs.

        Example:
            ```python
            MyModel = apps.get_model('my_app', 'MyModel')
            data = {"field1": "value1", "field2": "value2"}
            created_instance = ModelCrudMixin.create_model(MyModel, data)
            ```
        """
        logger.info('Mixin create_model method entered...')
        try:
            logger.info(f"Starting to create {model.__name__} with data: {data}")
            valid_fields = [field.name for field in model._meta.get_fields()]  # noqa
            filtered_data = {key: value for key, value in data.items() if key in valid_fields}
            created_object = model.objects.create(**filtered_data)
            logger.info(f"Successfully created {model.__name__} with ID: {created_object.pk}")
            return created_object
        except IntegrityError as ie:  # Django-wrapped IntegrityError
            logger.error(f"Integrity error: {str(ie)}")
            raise IntegrityError(f"A {model.__name__} with the same unique field already exists: {str(ie)}")
        except OperationalError as e:
            logger.error(f"Operational error occurred: {str(e)}")
            raise OperationalError(f"Database error occurred: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    @classmethod
    def get_or_create_model(cls, model, data):
        try:
            user, created = model.objects.get_or_create(
                email=data.get('email'),
                defaults=data
            )
            return user, created
        except OperationalError as e:
            raise OperationalError(f"Database error has occurred: {str(e)}")