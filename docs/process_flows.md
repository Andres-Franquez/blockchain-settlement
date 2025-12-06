# Process Flows – Post-Trade Workflow

## 1. Trade Capture Flow

**Actors:** External trading venues, internal trade capture systems.

**Steps:**
1. External systems generate a batch of executed trades.
2. The trades are exported into a CSV file (`trades_raw.csv`).
3. The prototype system ingests the CSV file and parses each row into an internal `Trade` object.
4. Basic validation rules are applied (e.g., buyer ≠ seller).
5. For each accepted trade, a `TRADE_CAPTURE` transaction is written into a new ledger block.

**Outcome:** All valid trades for the day are captured and logged on the ledger.

---

## 2. End-of-Day Netting Flow

**Actors:** Clearing & netting engine.

**Steps:**
1. At end-of-day, the system groups trades by `(participant_id, instrument_id)`.
2. For each group, the system computes:
   - `net_quantity` (buys minus sells)
   - `net_cash` (cash to be paid or received)
3. A `NetObligation` object is created for each `(participant, instrument)` pair.
4. A `NETTING` transaction is written to the ledger containing all net obligations for the day.

**Outcome:** Gross trade exposures are reduced to net obligations that are economically equivalent but easier to settle.

---

## 3. T+1 Settlement Flow

**Actors:** Settlement engine, participant accounts.

**Steps:**
1. The system assigns initial cash and securities balances to each participant (simulated).
2. On settlement date (T+1), each `NetObligation` is processed:
   - If the participant has sufficient cash and/or securities to meet the obligation, balances are updated and the obligation is marked `SETTLED`.
   - If balances are insufficient, the obligation is marked `FAILED`.
3. A `SETTLEMENT_RESULT` transaction is written to the ledger for each obligation.

**Outcome:** Successful and failed settlement obligations are explicitly recorded, and updated balances reflect the result of the settlement run.

---

## 4. Analytics & Reporting Flow

**Actors:** Risk and operations stakeholders.

**Steps:**
1. The system computes:
   - Netting efficiency: gross vs net cash exposure.
   - Fail statistics: total obligations, failed obligations, fail rate.
   - Exposure by participant: sum of absolute net cash obligations.
2. These metrics are printed to the console and can also be exported for dashboards.
3. Risk and operations teams use these metrics to evaluate the health of the post-trade process and to identify participants with elevated risk.

**Outcome:** Stakeholders gain insight into the performance and risk profile of the settlement process.
