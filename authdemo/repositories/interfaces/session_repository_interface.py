import abc


class SessionRepositoryInterface(abc.ABC):

    @abc.abstractmethod
    def create_session(self, data: dict):
        pass

    @abc.abstractmethod
    def get_or_create_session(self, data: dict):
        """Fetch a session based on provided data or create a session if not exists"""
        pass

    @abc.abstractmethod
    def get_session(self, session_id: int):
        pass

    @abc.abstractmethod
    def delete_session(self, session_id: int):
        pass
