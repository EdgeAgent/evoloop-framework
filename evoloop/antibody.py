class Antibody:
    """A test cloned from an observed failure. Formal only with signature+probe+status."""
    def __init__(self, name, failure, signature=None, probe=None):
        self.name = name; self.failure = failure; self.signature = signature; self.probe = probe; self.status = "seeking"
    def checks(self):
        return {"cloned_from_instance": bool(self.failure), "seeks_recurrence": bool(self.probe), "self_test": bool(self.probe), "status_lifecycle": self.status in ("seeking", "neutralized", "immune"), "routable": bool(self.signature and self.probe)}
    def is_formal(self):
        # Formal = all 5, and crucially signature + probe + a tracked status. Missing any -> functional only.
        return bool(self.signature and self.probe and self.failure)
    def shard(self):
        if not self.is_formal(): return None
        return {"name": self.name, "signature": self.signature, "probe": self.probe, "status": self.status, "failure": self.failure}
    def neutralize(self): self.status = "neutralized"
    def immunize(self):
        if self.is_formal(): self.status = "immune"; return True
        return False
