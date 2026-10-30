class Engram:
    def __init__(self): self.entries = []
    def record(self, entry, conflicts=0):
        self.entries.append(entry); return {"recorded": entry, "conflicts_judged": conflicts, "non_conflicts": conflicts == 0}
class LaneBoard:
    def __init__(self): self.announcements = []
    def announce(self, msg): self.announcements.append(msg); return msg
class ModelVersioner:
    def __init__(self): self.versions = []
    def register(self, name, eval_reward):
        v = f"{name} v{len(self.versions)+1}"; self.versions.append({"version": v, "eval_mean_reward": eval_reward}); return v
