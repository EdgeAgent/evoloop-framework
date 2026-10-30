import hashlib, json
def chain_receipt(steps):
    prev = "GENESIS"; out = []
    for s in steps:
        h = hashlib.sha256(json.dumps({"prev": prev, "step": s}, sort_keys=True).encode()).hexdigest(); prev = h; out.append({**s, "hash": h})
    return out, prev
