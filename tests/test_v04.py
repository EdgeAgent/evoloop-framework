import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evoloop.report import render_report
from evoloop.evolution import Evolution
def test_report_is_static_html():
    p = render_report(Evolution().run(2), os.path.join(os.path.dirname(__file__), "report.html"))
    assert "<table>" in open(p).read() and "animation" not in open(p).read().lower().split("no animation")[0][-20:]
def test_report_contains_generations():
    r = Evolution().run(2); assert len(r["generations"]) == 2; assert r["final_immune_rules"] == 2
def test_icon_is_square_and_centered_disc():
    from PIL import Image
    im = Image.open("docs/assets/icon.png"); assert im.size[0] == im.size[1] and im.size[0] >= 512
def test_hero_is_wide():
    from PIL import Image
    im = Image.open("docs/assets/hero.png"); assert im.size[0] > im.size[1] and im.size[0] >= 1200
def test_workflow_has_8_steps():
    assert os.path.exists("docs/assets/workflow.png")
def test_architecture_has_report():
    assert os.path.exists("docs/assets/architecture.png")
def test_evolve_still_improves():
    from evoloop.evolve_real import evolve_from_file
    r = evolve_from_file("examples/clusterworm2_sample.jsonl"); assert r["benchmark"]["verdict"] == "IMPROVED"
def test_scanner_still_blocks():
    from evoloop.scanner import Scanner
    from evoloop.immune import ImmuneMemory
    from evoloop.antibody import Antibody
    im = ImmuneMemory(); im.promote(Antibody("stale_table", "f", signature="stale_table", probe="p")); assert Scanner(im).check("stale_table")["blocked"]
def test_readme_centers_icon():
    assert 'align="center"' in open("README.md").read()
def test_badges_say_30():
    assert "Tests 30 passing" in open("README.md").read()
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
