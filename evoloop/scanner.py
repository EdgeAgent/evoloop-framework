class Scanner:
    """Real router: maps an error namespace to a formal immune shard BEFORE execution. Blocks, never warns-and-continues."""
    def __init__(self, immune): self.immune = immune
    def check(self, error_namespace):
        if self.immune.blocks(error_namespace):
            return {"blocked": True, "rule": self.immune.rules[error_namespace], "action": "BLOCKED by immune memory — do not execute, do not spend"}
        return {"blocked": False, "action": "no immune rule — proceed, record outcome"}
