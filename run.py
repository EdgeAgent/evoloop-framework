#!/usr/bin/env python3
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evoloop.pipeline import run_end_to_end
if __name__ == "__main__":
    r = run_end_to_end()
    print(json.dumps(r, indent=2))
    print("\nLOOP CLOSED:" if r["second_run_stale_blocked"] else "\nLOOP OPEN:")
    print(f"  {r['immune_rules']} formal immune rules → mock training eval {r['trained']['eval_mean_reward']} → {r['model_version']} → Engram + board recorded → stale failure blocked on second run: {r['second_run_stale_blocked']}")
