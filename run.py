#!/usr/bin/env python3
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evoloop.pipeline import run_end_to_end
from evoloop.evolution import Evolution
from evoloop.evolve_real import evolve_from_file
from evoloop.evolution import Evolution as _Ev
from evoloop.report import render_report as _rr
from evoloop.dashboard import serve as _dash
from evoloop.guarded import guarded as _guarded
from evoloop.scanner import Scanner
from evoloop.immune import ImmuneMemory
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        _dash(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "guarded":
        ns = sys.argv[2]; cmd = sys.argv[4:] if len(sys.argv) > 3 and sys.argv[3] == "--" else sys.argv[3:]
        sys.exit(_guarded(ns, cmd))
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        import json as _j; r = _Ev().run(3); print(_rr(r, "evolution-report.html")); print(_j.dumps(r, indent=2)); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "evolve":
        import json as _j; r = evolve_from_file(sys.argv[2] if len(sys.argv)>2 else "examples/clusterworm2_sample.jsonl"); print(_j.dumps(r, indent=2)); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "loop":
        import argparse
        ap = argparse.ArgumentParser(); ap.add_argument("--generations", type=int, default=3); a = ap.parse_args(sys.argv[2:])
        r = Evolution().run(a.generations)
        import json as _j; print(_j.dumps(r, indent=2)); print(f"\nEVOLUTION: gen1 created rules, gen2+ blocked recurrences, final {r['final_immune_rules']} rules, {r['final_version']}"); sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == "scan":
        im = ImmuneMemory(); from evoloop.antibody import Antibody
        ab = Antibody("stale_table", "stale tables spent silently", signature="stale_table", probe="probe_stale_table"); im.promote(ab)
        print(Scanner(im).check(sys.argv[2])); sys.exit(0)
    r = run_end_to_end()
    print(json.dumps(r, indent=2))
    print("\nLOOP CLOSED:" if r["second_run_stale_blocked"] else "\nLOOP OPEN:")
    print(f"  {r['immune_rules']} formal immune rules → mock training eval {r['trained']['eval_mean_reward']} → {r['model_version']} → Engram + board recorded → stale failure blocked on second run: {r['second_run_stale_blocked']}")
