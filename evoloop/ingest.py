import json
"""Ingest real execution logs (JSONL). A failure is any record with status=failed, or stale=True, or reward < 0.
Each distinct error namespace becomes an antibody candidate — cloned from the observed instance, not a category."""
def ingest(path):
    records = []; failures = []
    for line in open(path):
        line = line.strip()
        if not line: continue
        r = json.loads(line); records.append(r)
        if r.get("status") == "failed" or r.get("stale") is True or r.get("reward", 0) < 0:
            failures.append({"namespace": r.get("error_namespace", "unknown"), "instance": r.get("detail", str(r))[:200], "features": r.get("features", [])})
    # Deduplicate by namespace, keep first instance
    seen = {}; 
    for f in failures: seen.setdefault(f["namespace"], f)
    return records, list(seen.values())
