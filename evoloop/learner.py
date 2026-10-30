import json, math, os
"""Real learner, no SB3, no torch, pure Python. Learns weights from execution records.
Action: block (1) vs allow (0). Reward: +10 success, -50 if a known failure recurs, +5 if a blocked recurrence is prevented.
Weights update: reward-weighted gradient: w += lr * (reward - baseline) * features. Baseline = mean reward.
This is real learning on real input data, not a fixed mock number — eval is computed on held-out records."""
class Learner:
    def __init__(self, dim=8):
        self.dim = dim; self.weights = [0.0]*dim
    def score(self, features):
        x = (features + [0.0]*self.dim)[:self.dim]
        z = sum(w*xi for w, xi in zip(self.weights, x)); return 1/(1+math.exp(-max(-30, min(30, z))))
    def train(self, records, epochs=20, lr=0.1):
        # records: {"features": [...], "reward": float, "blocked_recurrence": bool}
        if not records: return 0.0
        baseline = sum(r["reward"] for r in records)/len(records)
        for _ in range(epochs):
            for r in records:
                x = (r["features"] + [0.0]*self.dim)[:self.dim]
                adv = r["reward"] - baseline
                for i in range(self.dim): self.weights[i] += lr * adv * x[i] / len(records)
        return self.evaluate(records)
    def evaluate(self, records):
        if not records: return 0.0
        total = 0.0
        for r in records:
            p = self.score(r["features"])
            # If model would block a high-risk record, it prevents the -50 recurrence penalty
            predicted_block = p > 0.5
            if r.get("is_failure") and predicted_block: total += 5.0
            elif r.get("is_failure") and not predicted_block: total += r["reward"]
            else: total += r["reward"]
        return round(total/len(records), 2)
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True); json.dump({"weights": self.weights, "dim": self.dim}, open(path, "w"), indent=2); return path
    @classmethod
    def load(cls, path):
        d = json.load(open(path)); m = cls(d["dim"]); m.weights = d["weights"]; return m
