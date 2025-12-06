import pandas as pd
from datetime import datetime
from .trade_model import Trade

def load_trades(path: str):
    df = pd.read_csv(path)
    trades = []

    for _, row in df.iterrows():
        t = Trade(
            trade_id=row["trade_id"],
            trade_date=datetime.strptime(row["trade_date"], "%Y-%m-%d").date(),
            settlement_date=datetime.strptime(row["settlement_date"], "%Y-%m-%d").date(),
            buyer_id=row["buyer_id"],
            seller_id=row["seller_id"],
            instrument_id=row["instrument_id"],
            quantity=int(row["quantity"]),
            price=float(row["price"])
        )
        trades.append(t)

    return trades
