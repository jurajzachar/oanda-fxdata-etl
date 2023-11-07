import logging
import os

import psycopg2


class Persistence():

    def __init__(self):
        self.conn = None
        self.db_name = os.environ.get("db_name")
        assert self.db_name is not None, "env var 'db_name' must be set"
        self.db_user = os.environ.get("db_user")
        assert self.db_user is not None, "env var 'db_user' must be set"
        self.db_pwd = os.environ.get("db_pwd")
        assert self.db_pwd is not None, "env var 'db_pwd' must be set"
        self.db_host = os.environ.get("db_host")
        assert self.db_host is not None, "env var 'db_host' must be set"
        self.db_port = os.environ.get("db_port")
        assert self.db_port is not None, "env var 'db_port' must be set"

    def __del__(self):
        if self.conn is not None:
            try:
                self.conn.close()
                logging.info("successfully closed database connection")
            except (Exception, psycopg2.DataError) as error:
                logging.error("failed to gracefully close database connection due to: %s " % error)

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
            result = self.conn.cursor().execute('select current_time').fetchAll()
            assert result is not None
            logging.info(
                "successfully established connection to the database=%s as user=%s at host=%s:%d, current_time=%s" % (
                    self.db_name, self.db_user, self.db_host, int(self.db_port), result)
            )
        except (Exception, psycopg2.DataError) as error:
            logging.error("failed to connect to the database due to: %s" % error)

    def upsert_to_db(self, folder, filename) -> (str, str):
        """ attempts to insert a new filesystem asset into oanda_fx_files if it does not exist.
        See hypertable.sql for details"""
        sql = """INSERT INTO oanda_fx_files(folder, filename) values(%s, %s) ON CONFLICT DO NOTHING 
        RETURNING (folder, filename)"""

        try:
            # create a new cursor
            cursor = self.conn.cursor()
            cursor.execute(sql, (folder, filename))
            result = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("failed to persist (%s, %s) due to %s" % folder, filename, error)
            return None
