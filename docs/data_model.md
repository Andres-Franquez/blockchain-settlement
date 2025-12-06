# Data Model

## Trade

Represents an individual executed trade.

| Field           | Type   | Description                         |
|----------------|--------|-------------------------------------|
| trade_id       | str    | Unique identifier for the trade     |
| trade_date     | date   | Trade execution date                |
| settlement_date| date   | Scheduled settlement date (T+1)     |
| buyer_id       | str    | Buying participant identifier       |
| seller_id      | str    | Selling participant identifier      |
| instrument_id  | str    | Instrument identifier (e.g. STOCK_A)|
| quantity       | int    | Number of shares traded             |
| price          | float  | Price per share                     |
| status         | str    | Lifecycle status (NEW, NETTED, etc.)|

## NetObligation

Represents a netted obligation per participant and instrument.

| Field          | Type   | Description                                             |
|----------------|--------|---------------------------------------------------------|
| participant_id | str    | Participant identifier                                  |
| instrument_id  | str    | Instrument identifier                                   |
| net_quantity   | int    | Net shares (positive = receives, negative = delivers)  |
| net_cash       | float  | Net cash (positive = receives, negative = pays)        |
| status         | str    | Settlement status (PENDING, SETTLED, FAILED)           |

## LedgerBlock

Represents a block in the hash-chained ledger.

| Field         | Type   | Description                                |
|---------------|--------|--------------------------------------------|
| block_id      | int    | Sequential block number                    |
| previous_hash | str    | Hash of the previous block (or GENESIS)    |
| timestamp     | str    | UTC timestamp of block creation            |
| transactions  | list   | List of transaction payloads in this block |
| hash          | str    | SHA-256 hash of the block contents         |

## Transaction (Logical)

Transactions are stored as dictionaries within `LedgerBlock.transactions` and can represent:

- `TRADE_CAPTURE` – trade ingestion events.
- `NETTING` – net obligation summaries.
- `SETTLEMENT_RESULT` – settlement outcomes per obligation.
