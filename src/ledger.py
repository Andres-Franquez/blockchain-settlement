import hashlib, json
from datetime import datetime

class LedgerBlock:
    def __init__(self, block_id, previous_hash, transactions):
        self.block_id = block_id
        self.previous_hash = previous_hash
        self.timestamp = datetime.utcnow().isoformat()
        self.transactions = transactions
        self.hash = self.compute_hash()

    def compute_hash(self):
        payload = json.dumps({
            "block_id": self.block_id,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

class Ledger:
    def __init__(self):
        self.blocks = []

    def add_block(self, transactions):
        prev_hash = self.blocks[-1].hash if self.blocks else "GENESIS"
        block = LedgerBlock(len(self.blocks), prev_hash, transactions)
        self.blocks.append(block)
        return block
