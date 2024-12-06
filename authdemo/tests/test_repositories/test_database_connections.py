import pytest
from django.db import connections
from django.db.utils import OperationalError
from django.utils.connection import ConnectionDoesNotExist


@pytest.fixture
def db_connections_fixture():
    """Return a list of strings of all available db connections names
    define in settings file.
    """
    return list(connections)


def test_db_connection(db_connections_fixture):
    """Check if connection to all db are successful."""

    for db_conn_name in db_connections_fixture:
        try:
            db_conn = connections[db_conn_name]
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT 1;")
        except ConnectionDoesNotExist:
            pytest.fail(f"Connection {db_conn_name} does not exist.")
        except OperationalError as e:
            pytest.fail(f"Operational error on {db_conn_name} : {e}")