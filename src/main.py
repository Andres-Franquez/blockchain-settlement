from src.data_loader import load_trades
from src.ledger import Ledger
from src.settlement_engine import net_trades, simulate_balances, run_settlement
from src.analytics import compute_netting_efficiency, compute_fail_stats, exposure_by_participant

def main():
    trades = load_trades("data/trades_raw.csv")
    ledger = Ledger()

    # 1. Log Trade Capture
    tx = [{"type": "TRADE_CAPTURE", "trade_id": t.trade_id} for t in trades]
    ledger.add_block(tx)

    # 2. Netting
    obligations = net_trades(trades)
    net_tx = [{"type": "NETTING", "participant": o.participant_id, "net_cash": o.net_cash} 
              for o in obligations]
    ledger.add_block(net_tx)

    # 3. Settlement
    balances = simulate_balances(obligations)
    run_settlement(obligations, balances)

    settle_tx = [{"type": "SETTLEMENT", "participant": o.participant_id, "status": o.status}
                 for o in obligations]
    ledger.add_block(settle_tx)

    # 4. Analytics
    print("\nNetting Efficiency:", compute_netting_efficiency(trades, obligations))
    print("Fail Stats:", compute_fail_stats(obligations))
    print("Exposure:", exposure_by_participant(obligations))

if __name__ == "__main__":
    main()
