import logging as log

import pytest
from testcontainers.postgres import PostgresContainer

log.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=log.INFO)


@pytest.fixture
def postgresql() -> None:
    log.info("[fixture] starting db container")
    postgres = PostgresContainer("postgres:16")
    postgres.start()
    log.info("[fixture] connecting to: {}".format(postgres.get_connection_url()))

def test_should_initialize_successfully(postgresql):
    assert postgresql is None

