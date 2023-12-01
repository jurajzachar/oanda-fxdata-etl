import logging
import os

import psycopg2


class Persistence:

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

    def __del__(self):
        if self.conn is not None:
            try:
                self.conn.close()
                logging.info("successfully closed database connection")
            except (Exception, psycopg2.DataError) as error:
                logging.error("failed to gracefully close database connection due to: %s " % error)

    @staticmethod
    def from_environment():
        return Persistence(
            os.environ.get("db_name"),
            os.environ.get("db_user"),
            os.environ.get("db_pwd"),
            os.environ.get("db_host"),
            os.environ.get("db_port")
        )

    def connect(self) -> 'Persistence':
        try:
            # connect to the PostgreSQL database
            self.conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_pwd,
                host=self.db_host,
                port=self.db_port
            )

            self.conn.set_session(isolation_level='SERIALIZABLE', autocommit=True)

            with self.conn.cursor() as curs:
                curs.execute('select current_time')
                res = curs.fetchone()
                assert res is not None
            logging.info(
                f"successfully established connection to the database={self.db_name} as user={self.db_user} at host="
                f"{self.db_host}:{self.db_port}, current_time={res}"
            )
            return self
        except psycopg2.Error as error:
            logging.error(f"failed to connect to the database due to:{error.args}")
            raise error

    def execute_migration(self, migration_file: str) -> 'Persistence':
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir, 'sql', migration_file), 'r') as f:
            sql = f.read()
            with self.conn.cursor() as curs:
                try:
                    curs.execute(sql)

                except psycopg2.Error as error:
                    logging.error(f"failed to execute database migration={migration_file} due to:{error.args}")
        return self

    def upsert_to_fx_files(self, folder, filename) -> (str, str):
        """ attempts to insert a new filesystem asset into oanda_fx_files if it does not exist.
        See schema.sql for details"""
        try:
            # create a new cursor
            cursor = self.conn.cursor()
            cursor.execute(
                f"INSERT INTO oanda.fx_files(path) values('{os.path.join(folder, filename)}') ON CONFLICT DO NOTHING RETURNING *")
            result = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            logging.error(f"failed to persist ({folder}, {filename}) due to {error.args}")
            return None
