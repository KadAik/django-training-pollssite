import abc


class UserRepositoryInterface(abc.ABC):

    @abc.abstractmethod
    def create_user(self, data: dict):
        pass

    @abc.abstractmethod
    def get_or_create_user(self, data: dict):
        """Fetch a user based on provided data or create a user if not exists"""
        pass

    @abc.abstractmethod
    def get_user(self, user_id: int):
        pass

    @abc.abstractmethod
    def delete_user(self, user_id: int):
        pass
