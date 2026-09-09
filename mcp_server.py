import sys
import json
from client import TwoPhaseCommitSink

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "tx_flow":
        sink = TwoPhaseCommitSink()
        sink.begin_transaction("tx1")
        for r in params.get("records", []):
            sink.write_record("tx1", r)
        sink.pre_commit("tx1")
        sink.commit("tx1")
        return {"committed": sink.committed_data}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
