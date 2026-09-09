from client import TwoPhaseCommitSink

def main():
    print("=== Testing Two-Phase Commit Sink ===")
    sink = TwoPhaseCommitSink()
    sink.begin_transaction("tx_stream_10")
    sink.write_record("tx_stream_10", {"event_id": 1, "action": "click"})
    sink.write_record("tx_stream_10", {"event_id": 2, "action": "purchase"})

    pre_res = sink.pre_commit("tx_stream_10")
    print("Precommit:", pre_res)
    assert pre_res['status'] == 'PRECOMMITTED'

    commit_res = sink.commit("tx_stream_10")
    print("Commit:", commit_res)
    assert commit_res['status'] == 'COMMITTED'
    assert len(sink.committed_data) == 2

    print("Two-Phase Commit Sink verified successfully!")

if __name__ == '__main__':
    main()
