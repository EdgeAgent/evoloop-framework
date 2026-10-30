#!/bin/bash
# EVOLVELOOP one-command setup: Python 3.10+, no dependencies, no SB3/torch required.
set -e
python3 --version
python3 tests/test_evoloop.py
python3 tests/test_real.py
python3 run.py evolve examples/clusterworm2_sample.jsonl
echo "EVOLVELOOP ready. Try: python3 run.py loop --generations 3  |  python3 run.py scan stale_table"
