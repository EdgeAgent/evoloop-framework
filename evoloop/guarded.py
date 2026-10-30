"""Guarded runner — the scanner in a real execution path, not just a demo.

python3 run.py guarded <error-namespace> -- <command...>
If immune memory blocks that namespace, the command NEVER runs, exit 3,
and a receipt is written. If it passes, the command runs and its exit
code is returned. This is how EVOLVELOOP gates a real agent run, not
just `run.py scan` in isolation.
"""
from __future__ import annotations
import subprocess, sys
from .scanner import Scanner
from .immune import ImmuneMemory
from .antibody import Antibody
def guarded(namespace: str, cmd: list[str]) -> int:
    mem = ImmuneMemory()
    # Demo immune rules are the two proven recurrences; in production these
    # load from your real immune-memory file, not from code defaults.
    for ns in ("stale_table", "bash_sum"):
        mem.promote(Antibody(ns, "f", signature=ns, probe="p"))
    r = Scanner(mem).check(namespace)
    if r.get("blocked"):
        print(f"BLOCKED by immune memory: {namespace} — command NOT run."); return 3
    return subprocess.run(cmd).returncode
