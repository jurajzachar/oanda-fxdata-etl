import unittest

from oanda_filesystem import *

class OandaFilesystemTest(unittest.TestCase):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    folder = os.environ.get('fixtures', 'fixtures')
    print(folder)

    def test_oanda_filesystem_should_list_dir(self):
        files = list_in_dir(self.folder)
        self.assertEqual(len(files), 1)
        self.assertEqual("oanda_streams_sample.json", files[0])