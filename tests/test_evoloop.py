import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evoloop.antibody import Antibody
from evoloop.immune import ImmuneMemory
from evoloop.pipeline import run_end_to_end
def test_functional_not_formal_without_signature():
    ab = Antibody("x", "fail"); assert not ab.is_formal(); assert ab.shard() is None
def test_promotion_gate():
    im = ImmuneMemory(); ab = Antibody("x", "fail"); ok, _ = im.promote(ab); assert not ok; assert im.count() == 0
    ab2 = Antibody("stale_table", "stale", signature="stale_table", probe="probe_stale_table"); ok, _ = im.promote(ab2); assert ok; assert im.count() == 1
def test_status_lifecycle():
    ab = Antibody("s", "f", signature="s", probe="p"); ab.neutralize(); assert ab.status == "neutralized"; assert ab.immunize(); assert ab.status == "immune"
def test_router_blocks_recurrence():
    im = ImmuneMemory(); ab = Antibody("stale_table", "f", signature="stale_table", probe="p"); im.promote(ab); assert im.blocks("stale_table"); assert not im.blocks("unknown")
def test_loop_closes():
    r = run_end_to_end(); assert r["immune_rules"] == 2; assert r["second_run_stale_blocked"] is True; assert r["model_version"].startswith("first_trained_reward")
def test_trainer_uses_immune_rules():
    r = run_end_to_end(); assert r["trained"]["immune_rules_applied"] == 2

def test_scanner_blocks_before_execution():
    from evoloop.scanner import Scanner
    from evoloop.immune import ImmuneMemory
    im = ImmuneMemory(); ab = Antibody("stale_table", "f", signature="stale_table", probe="p"); im.promote(ab)
    assert Scanner(im).check("stale_table")["blocked"] is True; assert Scanner(im).check("other")["blocked"] is False
def test_multi_generation_blocks_recurrences():
    from evoloop.evolution import Evolution
    r = Evolution().run(3); assert r["generations"][0]["blocked"] == 0; assert r["generations"][1]["blocked"] == 2; assert r["generations"][2]["blocked"] == 2; assert r["final_immune_rules"] == 2
def test_loop_cli_flag_exists():
    import subprocess, sys; out = subprocess.check_output([sys.executable, "run.py", "loop", "--generations", "2"], text=True); assert "EVOLUTION" in out

if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
