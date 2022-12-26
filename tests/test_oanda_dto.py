import os.path
import unittest
from os import path
from stream_parser import read_oanda_streams_file
from oanda_dto import *

class OandaDtoTest(unittest.TestCase):
    folder = os.environ.get('fixtures', 'fixtures')
    file = path.abspath(path.join(folder, 'oanda_streams_sample.json'))

    def test_oandapricesdto_should_unmarshall_from_stream_data(self):
        output = read_oanda_streams_file(self.file)
        self.assertIsNotNone(output)
        data = output[0]
        for json in data:

            dto = unmarshall_from_stream_data(json)

            self.assertIsNotNone(dto)
            self.assertIsNotNone(dto.time)
            self.assertIsNotNone(dto.instrument_code)
            # level 1 must never be none
            self.assertIsNotNone(dto.ask_price_l1)
            self.assertIsNotNone(dto.bid_price_l1)
            self.assertIsNotNone(dto.ask_liquidity_l1)
            self.assertIsNotNone(dto.bid_liquidity_l1)
            # closeout must never be none
            self.assertIsNotNone(dto.closeout_ask)
            self.assertIsNotNone(dto.closeout_bid)
            self.assertGreater(dto.closeout_midpoint(), float(dto.closeout_bid))

    def test_oandapricesdto_should_marshall_to_db_row(self):
        #TODO
        pass

    def test_oandapricesdto_should_unmarshall_from_db_row(self):
        #TODO
        pass