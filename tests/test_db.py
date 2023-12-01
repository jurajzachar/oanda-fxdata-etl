import logging
import logging as log
import os

import pytest
from testcontainers.postgres import PostgresContainer
from urllib.parse import urlparse
from db import Persistence

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


@pytest.fixture(scope="session")
def postgresql_session(request) -> Persistence:
    log.info("[fixture] starting db container")
    postgres = PostgresContainer("postgres:16.1")
    postgres.start()
    conn_url = postgres.get_connection_url()
    log.info("[fixture] connecting to: {}".format(conn_url))
    persistence = Persistence(
        postgres.POSTGRES_DB,
        postgres.POSTGRES_USER,
        postgres.POSTGRES_PASSWORD,
        'localhost',
        urlparse(conn_url).port
    ).connect()
    assert persistence is not None
    with persistence.conn.cursor() as curs:
        curs.execute('show server_version')
        res = curs.fetchone()[0]
        assert str(res).__contains__('16.1')

    persistence\
        .execute_migration('V1__create_new_schema.sql')\
        .execute_migration('V2__create_fx_files.sql')

    def stop_db():
        log.info("[fixture] stopping db container")
        postgres.stop()

    request.addfinalizer(stop_db)
    return persistence


def test_should_initialize_successfully(postgresql_session: Persistence):
    assert postgresql_session is not None
    # returns the tuple if insert is successful
    inserted = postgresql_session.upsert_to_fx_files('foo', 'bar')
    assert inserted[0] == os.path.join('foo', 'bar')
