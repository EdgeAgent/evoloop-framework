class ImmuneMemory:
    def __init__(self): self.rules = {}
    def promote(self, antibody):
        shard = antibody.shard()
        if shard is None: return False, "functional only — missing signature/probe/status, cannot promote"
        self.rules[antibody.signature] = shard; return True, "promoted to formal immune memory"
    def blocks(self, error_namespace):
        return error_namespace in self.rules
    def count(self): return len(self.rules)
