from .antibody import Antibody
from .immune import ImmuneMemory
from .trainer import MockTrainer
from .engram import Engram, LaneBoard, ModelVersioner
from .scanner import Scanner

class Evolution:
    """Multi-generation loop with persistence, conflict judging, and rollback."""
    def __init__(self):
        self.immune = ImmuneMemory(); self.versions = ModelVersioner(); self.engram = Engram(); self.board = LaneBoard(); self.history = []
    def generation(self, gen, failures):
        scanner = Scanner(self.immune)
        blocked = [f for f in failures if scanner.check(f["namespace"])["blocked"]]
        new_failures = [f for f in failures if not scanner.check(f["namespace"])["blocked"]]
        for f in new_failures:
            ab = Antibody(f["namespace"], f["instance"], signature=f["namespace"], probe=f"probe_{f['namespace']}")
            self.immune.promote(ab)
        records = [{"reward": 10.0} for _ in range(20)]
        trained = MockTrainer().train(records, self.immune.rules)
        # Conflict judging: a new model with lower eval than previous is a conflict, rollback to previous version
        prev_eval = self.history[-1]["eval"] if self.history else None
        if prev_eval is not None and trained["eval_mean_reward"] < prev_eval:
            version = self.versions.versions[-1]["version"] if self.versions.versions else "first_trained_reward v1"
            conflict = "ROLLBACK: eval dropped, previous version kept"
        else:
            version = self.versions.register("first_trained_reward", trained["eval_mean_reward"]); conflict = "no conflict"
        self.engram.record({"generation": gen, "model": version, "immune_rules": self.immune.count(), "blocked": len(blocked)}, conflicts=0 if conflict == "no conflict" else 1)
        self.board.announce(f"Gen {gen}: {version}, {self.immune.count()} immune rules, {len(blocked)} recurrences blocked, eval {trained['eval_mean_reward']} ({conflict})")
        self.history.append({"generation": gen, "eval": trained["eval_mean_reward"], "immune_rules": self.immune.count(), "blocked": len(blocked), "version": version, "conflict": conflict})
        return self.history[-1]
    def run(self, generations=3):
        base = [{"namespace": "bash_sum", "instance": "bash summing 1..20000"}, {"namespace": "stale_table", "instance": "stale tables spent silently"}]
        for gen in range(1, generations+1):
            # Same failures every generation: gen 1 creates antibodies, gen 2+ should block both
            self.generation(gen, base)
        return {"generations": self.history, "final_immune_rules": self.immune.count(), "final_version": self.versions.versions[-1]["version"] if self.versions.versions else None, "board": self.board.announcements}
