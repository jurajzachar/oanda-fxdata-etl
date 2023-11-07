import logging as log

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text


@pytest.fixture(scope="session")
def postgresql_session(request):
    log.info("[fixture] starting db container")
    postgres = PostgresContainer("postgres:16")
    postgres.start()
    conn_url = postgres.get_connection_url()
    log.info("[fixture] connecting to: {}".format(conn_url))
    engine = create_engine(postgres.get_connection_url())
    # verify we can connect to the test container
    with engine.connect() as conn:
        res = conn.execute(text('show server_version'))
        for row in res:
            assert str(row).__contains__('16.0')

    def stop_db():
        log.info("[fixture] stopping db container")
        postgres.stop()

    request.addfinalizer(stop_db)

    return engine.connect()  # return a new connection


def test_should_initialize_successfully(postgresql_session):
    assert postgresql_session is not None
