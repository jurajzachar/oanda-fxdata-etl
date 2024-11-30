import logging
import logging as log
import os
from urllib.parse import urlparse

import pytest
from testcontainers.postgres import PostgresContainer

from db import Persistence
from oanda_schema import unmarshall_from_wire

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


@pytest.fixture(scope="function")
def postgresql_session(request) -> Persistence:
    log.info("[fixture] starting db container")
    # pin version to 14.10 to achieve timescaledb compat:
    # https://docs.timescale.com/self-hosted/latest/install/installation-linux/
    postgres = PostgresContainer("postgres:14.10")
    postgres.start()
    conn_url = postgres.get_connection_url()
    log.info("[fixture] connecting to: {}".format(conn_url))
    persistence = Persistence(
        postgres.dbname,
        postgres.username,
        postgres.password,
        'localhost',
        urlparse(conn_url).port
    ).__enter__()
    assert persistence is not None
    with persistence.conn.cursor() as curs:
        curs.execute('show server_version')
        res = curs.fetchone()[0]
        assert str(res).__contains__('14.10')

    persistence \
        .execute_migration('V1__create_new_schema.sql') \
        .execute_migration('V2__create_fx_files.sql') \
        .execute_migration('V3__create_fx_prices.sql')

    def stop_db():
        log.info("[fixture] stopping db container")
        postgres.stop()

    request.addfinalizer(stop_db)
    return persistence


def test_should_upsert_to_fx_files(postgresql_session: Persistence):
    assert postgresql_session is not None
    # returns the tuple if insert is successful
    inserted = postgresql_session.upsert_to_fx_files('foo', 'bar')
    assert inserted[0] == os.path.join('foo', 'bar')


def test_should_fetch_unprocessed_fx_files(postgresql_session: Persistence):
    assert postgresql_session is not None
    postgresql_session.upsert_to_fx_files('/fake-folder', 'fake-file')
    unprocessed = postgresql_session.fetch_unprocessed(0)
    assert unprocessed[0][0] == os.path.join('/fake-folder', 'fake-file')
    assert postgresql_session.fetch_unprocessed(1) == []


def test_should_fetch_processed_fx_files(postgresql_session: Persistence):
    assert postgresql_session is not None
    postgresql_session.upsert_to_fx_files('/fake-folder2', 'fake-file2')
    postgresql_session.mark_fx_file_processed(os.path.join('/fake-folder2', 'fake-file2'))
    processed = postgresql_session.fetch_processed(0)
    assert processed[0][0] == os.path.join('/fake-folder2', 'fake-file2')
    assert postgresql_session.fetch_processed(1) == []


def test_should_mark_fx_file_processed(postgresql_session: Persistence):
    assert postgresql_session is not None
    # returns the tuple if insert is successful
    postgresql_session.upsert_to_fx_files('/folder1', 'file2')
    marked = postgresql_session.mark_fx_file_processed(os.path.join('/folder1', 'file2'))
    assert marked[0] is not None
    unprocessed = postgresql_session.fetch_unprocessed(0)
    assert len(unprocessed) == 0


def test_should_upsert_to_fx_prices(postgresql_session: Persistence):
    data = [{"type": "PRICE", "time": "2021-10-22T19:34:08.122332673Z",
             "bids": [{"price": "1.37556", "liquidity": 1000000}, {"price": "1.37555", "liquidity": 2000000},
                      {"price": "1.37554", "liquidity": 2000000}, {"price": "1.37552", "liquidity": 5000000}],
             "asks": [{"price": "1.37569", "liquidity": 1000000}, {"price": "1.37571", "liquidity": 4000000},
                      {"price": "1.37573", "liquidity": 5000000}], "closeoutBid": "1.37552", "closeoutAsk": "1.37573",
             "status": "tradeable", "tradeable": True, "instrument": "GBP_USD"},
            {"type": "PRICE", "time": "2021-10-22T19:34:08.166739770Z",
             "bids": [{"price": "84.724", "liquidity": 5000000}],
             "asks": [{"price": "84.738", "liquidity": 5000000}], "closeoutBid": "84.724", "closeoutAsk": "84.738",
             "status": "tradeable", "tradeable": True, "instrument": "AUD_JPY"}]

    bulk_model_data = list(map(lambda x: unmarshall_from_wire(x), data))
    inserted = postgresql_session.insert_to_fx_prices(bulk_data=bulk_model_data, returning_data=True)
    assert inserted == [('("2021-10-22 19:34:08.122333+00",GBP_USD)',),
                        ('("2021-10-22 19:34:08.16674+00",AUD_JPY)',)]
