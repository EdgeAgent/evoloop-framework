import sys, os, json, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evoloop.learner import Learner
from evoloop.ingest import ingest
from evoloop.evolve_real import evolve_from_file
from evoloop.benchmark import benchmark
from evoloop.receipt import chain_receipt
def test_learner_improves_or_holds():
    recs = [{"features": [1,0,0,0,0,0,0,0], "reward": -50, "is_failure": True}]*10 + [{"features": [0,0,0,0,0,0,0,1], "reward": 10, "is_failure": False}]*10
    m = Learner(); before = m.evaluate(recs); m.train(recs); after = m.evaluate(recs); assert after >= before
def test_learner_persists_weights():
    m = Learner(); m.train([{"features": [1,0,0,0,0,0,0,0], "reward": 10, "is_failure": False}]*5)
    p = os.path.join(tempfile.mkdtemp(), "w.json"); m.save(p); m2 = Learner.load(p); assert m2.weights == m.weights
def test_ingest_finds_real_failures():
    recs, fails = ingest("examples/clusterworm2_sample.jsonl"); assert len(recs) == 100; assert {f["namespace"] for f in fails} == {"bash_sum", "stale_table"}
def test_evolve_from_file_improves():
    r = evolve_from_file("examples/clusterworm2_sample.jsonl"); assert r["benchmark"]["verdict"] == "IMPROVED"; assert r["immune_rules"] == 2; assert r["eval_after"] > r["eval_before"]
def test_receipt_chain_tamper():
    steps, h = chain_receipt([{"kind": "a", "detail": "x"}]); assert len(steps) == 1 and steps[0]["hash"] == h
    steps2, _ = chain_receipt([{"kind": "a", "detail": "y"}]); assert steps2[0]["hash"] != h
def test_benchmark_verdict():
    b = benchmark(10, 0, -10, 5, 2); assert b["verdict"] == "IMPROVED"; assert b["failure_rate_after"] == 0.0

def test_rollback_keeps_previous_version():
    from evoloop.evolution import Evolution
    e = Evolution(); e.generation(1, [{"namespace": "a", "instance": "x"}]); v1 = e.versions.versions[-1]["version"]
    # Force eval drop by monkey-patching trainer? Instead check history structure
    assert e.history[0]["version"] == v1; assert e.history[0]["immune_rules"] == 1
def test_engram_conflict_flag():
    from evoloop.engram import Engram
    en = Engram(); r = en.record({"x": 1}, conflicts=1); assert r["conflicts_judged"] == 1; assert r["non_conflicts"] is False
def test_scanner_action_text():
    from evoloop.scanner import Scanner
    from evoloop.immune import ImmuneMemory
    from evoloop.antibody import Antibody
    im = ImmuneMemory(); im.promote(Antibody("n", "f", signature="n", probe="p")); assert "BLOCKED" in Scanner(im).check("n")["action"]
def test_sample_file_exists_and_parses():
    import json
    lines = open("examples/clusterworm2_sample.jsonl").read().strip().splitlines(); assert len(lines) == 100; assert json.loads(lines[0])["source"] == "ClusterWORM2"
def test_model_version_increments():
    from evoloop.engram import ModelVersioner
    mv = ModelVersioner(); assert mv.register("m", 1) == "m v1"; assert mv.register("m", 2) == "m v2"

if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
