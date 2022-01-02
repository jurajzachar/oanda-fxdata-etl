import os.path
import unittest
from mockito import mock, verify
from os import path
from pybuilder.core import task
from stream_parser import read_oanda_streams_file

class StreamParserTest(unittest.TestCase):
    folder = os.environ.get('fixtures', 'fixtures')
    file = path.abspath(path.join(folder, 'oanda_streams_sample.json'))
    print("**debug** using file path to fixture: %s" % file)

    def test_should_parse_valid_lines(self):
        output = read_oanda_streams_file(self.file)
        self.assertIsNotNone(output)
        data = output[0]
        self.assertIsNotNone(data)
        self.assertEqual(2, len(data), "expected number tick prices doesn't match")
        summary = output[1]
        self.assertIsNotNone(summary)
        self.assertEqual(2, summary.no_of_heartbeats, "expected number of heartbeats doesn't match")
        self.assertEqual(2, summary.not_of_ticks, "expected number of tick prices doesn't match")