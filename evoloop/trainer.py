class MockTrainer:
    """Deterministic mock, labelled mock. SB3 adapter stub: records agent_type='SB3', does not run PPO."""
    def train(self, records, immune_rules, timesteps=100):
        # Reward: base from records, bonus for immune rules applied, penalty for unblocked failures.
        base = sum(r.get("reward", 0) for r in records)
        bonus = 100 * len(immune_rules)
        eval_reward = round(base + bonus, 1)
        return {"model": "mock_trained_reward", "agent_type": "SB3 (stub, mock training)", "train_records": len(records), "feature_dim": 261, "timesteps": timesteps, "eval_mean_reward": eval_reward, "immune_rules_applied": len(immune_rules)}
