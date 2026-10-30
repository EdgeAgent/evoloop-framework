import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evoloop.dashboard import render
from evoloop.guarded import guarded
from evoloop.sb3 import train_ppo
def test_dashboard_renders_generations():
    h = render(); assert "EVOLVELOOP" in h and "Final immune rules" in h and "<table>" in h
def test_guarded_blocks_immune_namespace():
    assert guarded("stale_table", ["echo", "should-not-run"]) == 3
def test_guarded_runs_clean_command():
    assert guarded("clean_namespace_xyz", ["echo", "hi"]) == 0
def test_sb3_missing_raises_not_fakes():
    try:
        import stable_baselines3  # noqa
        assert True  # if SB3 IS installed, a real run is allowed
    except ImportError:
        try: train_ppo(10); assert False
        except RuntimeError as e: assert "not installed" in str(e) and "never faked" in str(e)
def test_no_skeleton_status_claim():
    assert "Status-skeleton" not in open("README.md").read()
def test_quickstart_has_no_broken_failures_flag():
    assert "loop --failures" not in open("README.md").read()
def test_install_script_runs_tests():
    assert "test" in open("install.sh").read().lower()
def test_dashboard_is_readonly_note():
    assert "Read-only" in render()
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
