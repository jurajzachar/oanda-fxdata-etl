import logging
import os
from contextlib import AbstractContextManager
from typing import List

import psycopg2

from oanda_schema import OandaPriceTick


class Persistence(AbstractContextManager):

    def __init__(self, db_name, db_user, db_pwd, db_host, db_port):
        self.conn = None
        self.db_name = db_name
        assert self.db_name is not None, "'db_name' must be set"
        self.db_user = db_user
        assert self.db_user is not None, "'db_user' must be set"
        self.db_pwd = db_pwd
        assert self.db_pwd is not None, "'db_pwd must be set"
        self.db_host = db_host
        assert self.db_host is not None, "'db_host' must be set"
        self.db_port = db_port
        assert self.db_port is not None, "'db_port' must be set"

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn is not None:
            try:
                self.conn.close()
                logging.info("successfully closed database connection")
            except (Exception, psycopg2.DataError) as error:
                logging.error("failed to gracefully close database connection due to: %s " % error)

    def __enter__(self) -> 'Persistence':
        try:
            # connect to the PostgreSQL database
            self.conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_pwd,
                host=self.db_host,
                port=self.db_port
            )
            self.conn.set_session(isolation_level='READ COMMITTED', autocommit=True)
            return self
        except psycopg2.Error as error:
            logging.error(f"failed to connect to the database due to:{error.args}")
            raise error

    @staticmethod
    def from_environment():
        return Persistence(
            os.environ.get("db_name"),
            os.environ.get("db_user"),
            os.environ.get("db_pwd"),
            os.environ.get("db_host"),
            os.environ.get("db_port")
        )

    def execute_migration(self, migration_file: str) -> 'Persistence':
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir, 'sql', migration_file), 'r') as f:
            sql = f.read()
            with self.conn.cursor() as cursor:
                try:
                    cursor.execute(sql)
                except psycopg2.Error as error:
                    self.conn.rollback()
                    logging.error(f"failed to execute database migration={migration_file} due to:{error.args}")
                finally:
                    cursor.close()
        return self

    def insert_to_fx_prices(self, bulk_data: List[OandaPriceTick], returning_data: bool=False) -> (str, str):
        """
        Attempts to insert a bulk of OandaPriceTick into oanda_fx_prices if it does not exist.
        See oanda_schema.sql for details.

        :param bulk_data:
        :return: a tuple consisting of timestamps and instrument code
        """

        def to_postgres_tuple(x: OandaPriceTick) -> str:
            return (f"('{x.time}'::timestamptz,"
                    f"'{x.instrument}',"
                    f"{x.bid_price_l1},"
                    f"{x.bid_price_l2},"
                    f"{x.bid_price_l3},"
                    f"{x.ask_price_l1},"
                    f"{x.ask_price_l2},"
                    f"{x.ask_price_l3},"
                    f"{x.bid_liquidity_l1},"
                    f"{x.bid_liquidity_l2},"
                    f"{x.bid_liquidity_l3},"
                    f"{x.ask_liquidity_l1},"
                    f"{x.ask_liquidity_l2},"
                    f"{x.ask_liquidity_l3},"
                    f"{x.closeout_bid},"
                    f"{x.closeout_ask})"
                    .replace("None", 'null')
                    )

        data_to_insert = list(map(to_postgres_tuple, [x for x in bulk_data if x is not None]))
        insert_query = f"INSERT INTO oanda.fx_prices VALUES {','.join(data_to_insert)} ON CONFLICT DO NOTHING " \
                       f"RETURNING (\"time\",\"instrument\")"

        result = None

        try:
            # create a new cursor
            with self.conn.cursor() as cursor:
                cursor.execute(insert_query, data_to_insert)
                if returning_data:
                    result = cursor.fetchall()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            logging.error(f"failed to persist ({len(bulk_data)} items due to {error.args}")

        return result

    def upsert_to_fx_files(self, folder, filename) -> (str, str):
        """ attempts to insert a new filesystem asset into oanda_fx_files if it does not exist.
        See oanda_schema.sql for details"""
        result = None
        try:
            # create a new cursor
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO oanda.fx_files(path) values('{os.path.join(folder, filename)}') ON CONFLICT DO NOTHING "
                    f"RETURNING *")
                result = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            logging.error(f"failed to persist ({folder}, {filename}) due to {error.args}")
        finally:
            cursor.close()
        return result

    def mark_fx_file_processed(self, path: str) -> (str, str):
        """ attempts to mark the existing folder/filename as processed with the current timestamp """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE oanda.fx_files SET time_processed = current_timestamp where path = '{path}'"
                    f"RETURNING *")
                result = cursor.fetchone()
                return result
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            logging.error(f"failed to mark '{path}' as processed due to {error.args}")
            return None
        finally:
            cursor.close()

    def fetch_all_unprocessed(self):
        """fetches a page of unprocessed folder/filename entries using the provided offset"""
        with self.conn.cursor() as curs:
            sql = f"select path from oanda.fx_files where time_processed is null order by path"
            try:
                curs.execute(sql)
                return curs.fetchall()
            except psycopg2.Error as error:
                logging.error(f"failed to fetch unprocessed path entries with {sql}, due to:{error.args}")

    def fetch_unprocessed(self, offset: int, limit: int = 25):
        """fetches a page of unprocessed folder/filename entries using the provided offset"""
        with self.conn.cursor() as curs:
            sql = f"select path from oanda.fx_files where time_processed is null order by path limit {limit} offset {offset}"
            try:
                curs.execute(sql)
                return curs.fetchall()
            except psycopg2.Error as error:
                logging.error(f"failed to fetch unprocessed path entries with {sql}, due to:{error.args}")

    def fetch_processed(self, offset: int, limit: int = 25):
        """fetches a page of unprocessed folder/filename entries using the provided offset"""
        with self.conn.cursor() as curs:
            sql = f"select path from oanda.fx_files where time_processed is not null order by path limit {limit} offset {offset}"
            try:
                curs.execute(sql)
                return curs.fetchall()
            except psycopg2.Error as error:
                logging.error(f"failed to fetch unprocessed path entries with {sql}, due to:{error.args}")
