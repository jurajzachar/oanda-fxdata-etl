import unittest
import psycopg2
import logging
import os
from oanda_filesystem import *
from db import *

class OandaDbTest(unittest.TestCase):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    folder = os.environ.get('fixtures', 'fixtures')
    conn = None

    # set os environ to test db
    os.environ.setdefault('db_name', 'fxdata')
    os.environ.setdefault('db_user', 'timescaledb')
    os.environ.setdefault('db_pwd', 'timescaledb123')
    os.environ.setdefault('db_host', 'localhost')
    os.environ.setdefault('db_port', '5432')

    # verify test env is setup
    def setUp(self):
        # verify connection to the test PostgreSQL database
        try:
            self.conn = psycopg2.connect(
                database=os.environ.get('db_name'),
                user=os.environ.get('db_user'),
                password=os.environ.get('db_pwd'),
                host=os.environ.get('db_host'),
                port=os.environ.get('db_port')
            )
            logging.info("successfully verified connection to the database")
            cur = self.conn.cursor()
            cur.execute("TRUNCATE oanda.oanda_fx_files")
            self.conn.commit()
            cur.close()
            self.conn.close()
            logging.debug("closed db test connection")
        except (Exception, psycopg2.DatabaseError) as error:
            self.fail("failed to connect to the test database due to: %s" % error)

    def test_oanda_filesystem_should_list_dir(self):
        files = list_in_dir(self.folder)
        self.assertEqual(len(files), 1)
        self.assertEqual("oanda_streams_sample.json", files[0])

    def test_db_should_successfully_open_connection_to_the_test_db(self):
        persistence = Persistence()
        self.assertIsNotNone(persistence.conn)

    def test_db_should_successfully_upsert_file_to_the_test_db(self):
        persistence = Persistence()
        for file in list_in_dir(self.folder):
            result = persistence.upsert_to_db(self.folder, file)
            self.assertIsNotNone(result)
