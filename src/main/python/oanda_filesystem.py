import os.path
import logging
import psycopg2
from os import listdir
from os.path import isfile, join

def list_in_dir(dir):
    if not os.path.isdir(dir):
        raise RuntimeError("%s is not a directory" % dir)

    return [f for f in listdir(dir) if isfile(join(dir, f))]

class Persistence():
    dbname = None
    dbuser = None
    dbpwd = None
    dbhost = None
    dbport = None

    conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            logging.info("successfully closed database connection")

    def __init__(self):
        self.dbname = os.environ.get("dbname")
        self.dbuser = os.environ.get("dbuser")
        self.dbpwd = os.environ.get("dbpwd")
        self.dbhost = os.environ.get("dbhost")
        self.dbport = os.environ.get("dbport")

        if self.dbname is None:
            raise RuntimeError("env var 'dbname' is set?")

        if self.dbuser is None:
            raise RuntimeError("env var 'dbuser' is set?")

        if self.dbpwd is None:
            raise RuntimeError("env var 'dbpwd' is set?")

        if self.dbhost is None:
            raise RuntimeError("env var 'dbhost' is set?")

        if self.dbport is None:
            raise RuntimeError("env var 'dbport' is set?")

        try:
            # connect to the PostgreSQL database
            self.conn = psycopg2.connect(
                database=self.dbname,
                user=self.dbuser,
                password=self.dbpwd,
                host=self.dbhost,
                port=self.dbport
            )
            logging.info("successfully established connection to the database=%s as user=%s at host=%s:%d" % (
                self.dbname, self.dbuser, self.dbhost, int(self.dbport))
            )
        except (Exception, psycopg2.DataError) as error:
            logging.error("failed to connect to the database due to: " + error)

    def upsert_to_db(self, folder, filename)-> (str, str):
        """ attempts to insert a new filesystem asset into oanda_fx_files if it does not exist.
        See schema.sql for details"""
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
            logging.error("failed to persist (%s, %s) due to %s", folder, filename, error)
            return None
