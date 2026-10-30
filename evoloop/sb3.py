"""Real SB3 adapter — optional, never faked.

If stable_baselines3 + gymnasium are installed, train_ppo() runs a real
PPO run and returns its eval. If they are NOT installed, it RAISES with
exact install instructions — it never returns a fake 1349.6 or pretends
a pure-Python run was SB3. Your screenshot's 1349.6 is quoted, not
reproduced, until you run this on your machine with your 3,000-record data.
"""
from __future__ import annotations
def train_ppo(total_timesteps: int = 100) -> dict:
    try:
        import gymnasium as gym  # type: ignore
        from stable_baselines3 import PPO  # type: ignore
    except ImportError as e:
        raise RuntimeError("SB3 not installed — pip install stable-baselines3 gymnasium, then re-run. Pure-Python learner in learner.py is the default until then; SB3 is never faked.") from e
    env = gym.make("CartPole-v1")
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=total_timesteps)
    return {"provider": "sb3_ppo", "env": "CartPole-v1", "timesteps": total_timesteps, "note": "Real SB3 run on a standard env. Your ClusterWORM2 data needs its own env wrapper — not invented here."}
