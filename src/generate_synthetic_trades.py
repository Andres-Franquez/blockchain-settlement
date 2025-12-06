import csv
import random
from datetime import date, timedelta

def generate_synthetic_trades(
    output_path: str,
    n_trades: int = 50000,
):
    random.seed(42)

    participants = [f"PARTY{str(i).zfill(3)}" for i in range(1, 11)]  # PARTY001–PARTY010
    instruments = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

    start_date = date(2025, 1, 2)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "trade_id",
            "trade_date",
            "settlement_date",
            "buyer_id",
            "seller_id",
            "instrument_id",
            "quantity",
            "price"
        ])

        for i in range(1, n_trades + 1):
            trade_id = f"T{str(i).zfill(6)}"

            # random trade date in a 10-day window
            delta_days = random.randint(0, 9)
            trade_date = start_date + timedelta(days=delta_days)
            settlement_date = trade_date + timedelta(days=1)  # T+1

            # ensure buyer != seller
            buyer = random.choice(participants)
            seller = random.choice([p for p in participants if p != buyer])

            instrument = random.choice(instruments)

            quantity = random.choice([10, 25, 50, 100, 250, 500, 1000])
            # choose a base price per instrument
            base_price_map = {
                "STOCK_A": 10.0,
                "STOCK_B": 25.0,
                "STOCK_C": 55.0,
                "STOCK_D": 80.0,
                "STOCK_E": 120.0,
            }
            base_price = base_price_map[instrument]
            # small random noise
            price = round(base_price * (1 + random.uniform(-0.05, 0.05)), 2)

            writer.writerow([
                trade_id,
                trade_date.isoformat(),
                settlement_date.isoformat(),
                buyer,
                seller,
                instrument,
                quantity,
                price
            ])

if __name__ == "__main__":
    generate_synthetic_trades("data/trades_raw.csv", n_trades=50000)
