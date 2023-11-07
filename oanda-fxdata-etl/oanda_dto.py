"""encapsulation of Oanda Prices DTO"""
# see hypertable.sql
from builtins import RuntimeError
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dateutil import parser

@dataclass(frozen=True)
class OandaPricesDto:
    """Class for carrying price data point by Oanda"""
    time: datetime
    instrument_code: str
    bid_price_l1: float
    bid_price_l2: float
    bid_price_l2: float
    bid_price_l3: float
    ask_price_l1: float
    ask_price_l2: float
    ask_price_l3: float
    bid_liquidity_l1: int
    bid_liquidity_l2: int
    bid_liquidity_l3: int
    ask_liquidity_l1: int
    ask_liquidity_l2: int
    ask_liquidity_l3: int
    closeout_bid: float
    closeout_ask: float
    trading_venue: str = 'oanda'

    def closeout_midpoint(self) -> float:
        return float(self.closeout_ask) - float(self.closeout_bid) / 2 + float(self.closeout_bid)

def unmarshall_from_stream_data(json) -> Optional[OandaPricesDto]:
    def parse_level(arr, idx):
        try:
            return (arr[idx]["price"], arr[idx]["liquidity"])
        except:
            return (None, None)

    try:
        bids_l1 = parse_level(json["bids"], 0)
        bids_l2 = parse_level(json["bids"], 1)
        bids_l3 = parse_level(json["bids"], 2)
        asks_l1 = parse_level(json["asks"], 0)
        asks_l2 = parse_level(json["asks"], 1)
        asks_l3 = parse_level(json["asks"], 2)

        return OandaPricesDto(
            time=parser.isoparse(json["time"]),
            instrument_code=json["instrument"],
            # parse bids
            bid_price_l1=bids_l1[0],
            bid_liquidity_l1=bids_l1[1],
            bid_price_l2=bids_l2[0],
            bid_liquidity_l2=bids_l2[1],
            bid_price_l3=bids_l3[0],
            bid_liquidity_l3=bids_l3[1],
            # parse asks
            ask_price_l1=asks_l1[0],
            ask_liquidity_l1=asks_l1[1],
            ask_price_l2=asks_l2[0],
            ask_liquidity_l2=asks_l2[1],
            ask_price_l3=asks_l3[0],
            ask_liquidity_l3=asks_l3[1],
            # parse closeout prices
            closeout_bid=json["closeoutBid"],
            closeout_ask=json["closeoutAsk"]
        )
    except:
        # propagate
        raise RuntimeError("failed to parse json %s" % json)
        return None


def marshall_to_db_row(row):
    # TODO
    return None


def unmarshall_from_db_row(row):
    # TODO
    return None