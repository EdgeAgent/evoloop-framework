#!/bin/bash
# EVOLVELOOP one-command setup: Python 3.10+, no dependencies, no SB3/torch required.
set -e
python3 --version
python3 tests/test_evoloop.py
python3 tests/test_real.py
python3 run.py evolve examples/clusterworm2_sample.jsonl
echo "EVOLVELOOP ready. Try: python3 run.py loop --generations 3  |  python3 run.py scan stale_table"

echo "Dashboard: python3 run.py dashboard  (http://127.0.0.1:8769, read-only)"
echo "Guarded: python3 run.py guarded stale_table -- echo hello  (should BLOCK)"
echo "SB3: optional — pip install stable-baselines3 gymnasium, then use evoloop/sb3.py. Never faked."
