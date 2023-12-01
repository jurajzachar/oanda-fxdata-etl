"""encapsulation of Oanda Prices DTO"""
import logging

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class OandaPriceTick(BaseModel):
    """Class for carrying best 3 levels of prices and liquidity at Oanda,
    also see schema.sql"""
    # mandatory fields
    bid_price_l1: float
    bid_liquidity_l1: int
    ask_price_l1: float
    ask_liquidity_l1: int
    time: datetime
    instrument: str
    closeout_bid: float
    closeout_ask: float
    # optional
    bid_price_l2: Optional[float]
    bid_price_l3: Optional[float]
    ask_price_l2: Optional[float]
    ask_price_l3: Optional[float]
    bid_liquidity_l2: Optional[int]
    bid_liquidity_l3: Optional[int]
    ask_liquidity_l2: Optional[int]
    ask_liquidity_l3: Optional[int]

    def closeout_midpoint(self) -> float:
        return float(self.closeout_ask) - float(self.closeout_bid) / 2 + float(self.closeout_bid)

    def toJson(self) -> str:
        return self.model_dump_json(indent=2)

    def toDict(self) -> dict:
        return self.model_dump()

def unmarshall_from_wire(data: dict) -> Optional[OandaPriceTick]:
    def parse_level(idx: int, source: dict, target: dict) -> None:
        try:
            target[f'bid_price_l{idx+1}'] = float(source['bids'][idx]['price'])
            target[f'bid_liquidity_l{idx + 1}'] = source['bids'][idx]['liquidity']
            target[f'ask_price_l{idx+1}'] = float(source['asks'][idx]['price'])
            target[f'ask_liquidity_l{idx+1}'] = source['asks'][idx]['liquidity']
        except (KeyError, IndexError):
            pass
    try:
        flattened = {key: data[key] for key in ['time', 'instrument', 'closeoutBid', 'closeoutAsk'] if key in data}
        # remap to underscores
        for old_key, new_key in {'closeoutBid': 'closeout_bid', 'closeoutAsk': 'closeout_ask'}.items():
            if old_key in flattened:
                flattened[new_key] = flattened.pop(old_key)
        # set optional to None
        for idx in range(1,3):
            flattened[f'bid_price_l{idx+1}'] = None
            flattened[f'bid_liquidity_l{idx + 1}'] = None
            flattened[f'ask_price_l{idx+1}'] = None
            flattened[f'ask_liquidity_l{idx+1}'] = None
        for idx in range(0, 3):
            parse_level(idx, data, flattened)

        return OandaPriceTick(**flattened)
    except Exception as e:
        # propagate
        logging.error(f"failed to parse data={data}; {e.args}")
        return None


def marshall_to_db_row(row):
    # TODO
    return None


def unmarshall_from_db_row(row):
    # TODO
    return None