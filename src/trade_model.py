from dataclasses import dataclass
from datetime import date

@dataclass
class Trade:
    trade_id: str
    trade_date: date
    settlement_date: date
    buyer_id: str
    seller_id: str
    instrument_id: str
    quantity: int
    price: float
    status: str = "NEW"

@dataclass
class NetObligation:
    participant_id: str
    instrument_id: str
    net_quantity: int
    net_cash: float
    status: str = "PENDING"
