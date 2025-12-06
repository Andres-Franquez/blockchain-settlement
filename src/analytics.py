def compute_netting_efficiency(trades, obligations):
    gross = sum(t.quantity * t.price for t in trades)
    net = sum(abs(o.net_cash) for o in obligations)
    eff = 1 - (net / gross)
    return {"gross_cash": gross, "net_cash": net, "efficiency": eff}

def compute_fail_stats(obligations):
    total = len(obligations)
    fails = sum(1 for o in obligations if o.status == "FAILED")
    return {"total": total, "fails": fails, "fail_rate": fails / total}

def exposure_by_participant(obligations):
    exposure = {}
    for o in obligations:
        exposure.setdefault(o.participant_id, 0)
        exposure[o.participant_id] += abs(o.net_cash)
    return exposure
