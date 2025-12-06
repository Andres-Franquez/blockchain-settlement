from collections import defaultdict
from .trade_model import NetObligation

def net_trades(trades):
    nets = defaultdict(lambda: {"qty": 0, "cash": 0})

    for t in trades:
        nets[(t.buyer_id, t.instrument_id)]["qty"] += t.quantity
        nets[(t.buyer_id, t.instrument_id)]["cash"] -= t.quantity * t.price

        nets[(t.seller_id, t.instrument_id)]["qty"] -= t.quantity
        nets[(t.seller_id, t.instrument_id)]["cash"] += t.quantity * t.price

    obligations = []
    for (party, instr), v in nets.items():
        obligations.append(NetObligation(
            participant_id=party,
            instrument_id=instr,
            net_quantity=v["qty"],
            net_cash=v["cash"]
        ))
    return obligations

def simulate_balances(obligations):
    parties = {o.participant_id for o in obligations}
    instruments = {o.instrument_id for o in obligations}

    balances = {}
    for p in parties:
        balances[p] = {"CASH": 1_000_000}
        for instr in instruments:
            balances[p][instr] = 10_000
    return balances

def run_settlement(obligations, balances):
    for o in obligations:
        need_qty = -o.net_quantity if o.net_quantity < 0 else 0
        need_cash = -o.net_cash if o.net_cash < 0 else 0

        has_qty = balances[o.participant_id][o.instrument_id] >= need_qty
        has_cash = balances[o.participant_id]["CASH"] >= need_cash

        if has_qty and has_cash:
            balances[o.participant_id][o.instrument_id] -= need_qty
            balances[o.participant_id]["CASH"] -= need_cash

            if o.net_quantity > 0:
                balances[o.participant_id][o.instrument_id] += o.net_quantity

            if o.net_cash > 0:
                balances[o.participant_id]["CASH"] += o.net_cash

            o.status = "SETTLED"
        else:
            o.status = "FAILED"
