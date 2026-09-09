class TwoPhaseCommitSink:
    """Transactional 2PC Sink for End-to-End Exactly-Once Processing."""
    def __init__(self):
        self.committed_data = []
        self.pending_transactions = {}
        self.precommitted_transactions = set()

    def begin_transaction(self, tx_id):
        self.pending_transactions[tx_id] = []
        return {'status': 'STARTED', 'tx_id': tx_id}

    def write_record(self, tx_id, record):
        if tx_id not in self.pending_transactions:
            raise ValueError(f"Tx {tx_id} not found")
        self.pending_transactions[tx_id].append(record)

    def pre_commit(self, tx_id):
        if tx_id not in self.pending_transactions:
            raise ValueError("Invalid tx")
        self.precommitted_transactions.add(tx_id)
        return {'status': 'PRECOMMITTED', 'tx_id': tx_id, 'count': len(self.pending_transactions[tx_id])}

    def commit(self, tx_id):
        if tx_id not in self.precommitted_transactions:
            raise ValueError("Tx not precommitted")
        records = self.pending_transactions.pop(tx_id)
        self.precommitted_transactions.remove(tx_id)
        self.committed_data.extend(records)
        return {'status': 'COMMITTED', 'tx_id': tx_id, 'total_committed': len(self.committed_data)}

    def abort(self, tx_id):
        self.pending_transactions.pop(tx_id, None)
        self.precommitted_transactions.discard(tx_id)
        return {'status': 'ABORTED', 'tx_id': tx_id}
