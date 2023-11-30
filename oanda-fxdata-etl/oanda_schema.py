"""encapsulation of Oanda Prices DTO"""
# see schema.sql
from builtins import RuntimeError
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class OandaPriceTick(BaseModel):
    """Class for carrying best 3 levels of prices and liquidity at Oanda"""
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
    bid_price_l2: Optional[float] = Field(default=None)
    bid_price_l3: Optional[float] = Field(default=None)
    ask_price_l2: Optional[float] = Field(default=None)
    ask_price_l3: Optional[float] = Field(default=None)
    bid_liquidity_l2: Optional[int] = Field(default=None)
    bid_liquidity_l3: Optional[int] = Field(default=None)
    ask_liquidity_l2: Optional[int] = Field(default=None)
    ask_liquidity_l3: Optional[int] = Field(default=None)

    def closeout_midpoint(self) -> float:
        return float(self.closeout_ask) - float(self.closeout_bid) / 2 + float(self.closeout_bid)

    def toJson(self) -> str:
        return self.model_dump_json(indent=2)

    def toDict(self) -> dict:
        return self.model_dump()

def unmarshall_from_wire(data: dict) -> Optional[OandaPriceTick]:
    def parse_level(idx: int, source: dict, target: dict) -> None:
        try:
            target[f"bid_price_l{idx+1}"] = float(source["bids"][idx]["price"])
            target[f"ask_price_l{idx+1}"] = float(source["asks"][idx]["price"])
            target[f"bid_liquidity_l{idx+1}"] = source["bids"][idx]["liquidity"]
            target[f"ask_liquidity_l{idx+1}"] = source["asks"][idx]["liquidity"]
        except (KeyError, IndexError):
            pass
    try:
        flattened = {key: data[key] for key in ["time, instrument", "closeout_bid", "closeout_ask"] if key in data}
        for idx in range(0 , 2):
            parse_level(idx, data, flattened)

        return OandaPriceTick(**flattened)
    except Exception as e:
        # propagate
        raise RuntimeError(f"failed to parse data={data}; {e.args}")
        return None


def marshall_to_db_row(row):
    # TODO
    return None


def unmarshall_from_db_row(row):
    # TODO
    return None