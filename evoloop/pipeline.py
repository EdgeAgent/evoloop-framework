from .antibody import Antibody
from .immune import ImmuneMemory
from .trainer import MockTrainer
from .engram import Engram, LaneBoard, ModelVersioner

def run_end_to_end(source="ClusterWORM2", event_type="clusterworm2_worm_executed", failures=None):
    failures = failures or [{"namespace": "bash_sum", "instance": "bash summing 1..20000"}, {"namespace": "stale_table", "instance": "stale tables spent silently"}]
    immune = ImmuneMemory(); antibodies = []
    for f in failures:
        ab = Antibody(f["namespace"], f["instance"], signature=f["namespace"], probe=f"probe_{f['namespace']}")
        ok, msg = immune.promote(ab); antibodies.append((ab, ok, msg))
    records = [{"reward": 10.0} for _ in range(20)]
    trained = MockTrainer().train(records, immune.rules)
    version = ModelVersioner().register("first_trained_reward", trained["eval_mean_reward"])
    engram = Engram(); engram.record({"model": version, "immune_rules": immune.count()}, conflicts=0)
    board = LaneBoard(); board.announce(f"Model {version} registered, {immune.count()} immune rules, eval {trained['eval_mean_reward']}")
    # Second run: immune memory blocks recurrence
    blocked = immune.blocks("stale_table")
    return {"source": source, "event_type": event_type, "antibodies": [(a.name, a.status, ok) for a, ok, _ in antibodies], "immune_rules": immune.count(), "trained": trained, "model_version": version, "engram_entries": len(engram.entries), "board": board.announcements, "second_run_stale_blocked": blocked}
