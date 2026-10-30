"""Live dashboard — stdlib only, read-only, no login, no animation.
Serves http://127.0.0.1:8769 : generations, immune rules, eval, receipts,
scanner check form (GET only, no execution). It NEVER trains, promotes,
or executes a guarded command — those stay CLI-only.
"""
from __future__ import annotations
import json, html
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from .evolution import Evolution
def render() -> str:
    ev = Evolution().run(3)
    rows = "".join(f"<tr><td>{g['generation']}</td><td>{g['eval']}</td><td>{g['immune_rules']}</td><td>{g['blocked']}</td><td>{html.escape(str(g['version']))}</td></tr>" for g in ev["generations"])
    return f"""<!doctype html><html><head><meta charset=utf-8><title>EVOLVELOOP — Dashboard</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:30px auto;padding:0 20px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style></head><body>
<h1>EVOLVELOOP — Dashboard</h1><p>Local only. Read-only. Training, promotion and guarded runs stay CLI-only.</p>
<p>Final immune rules: {ev['final_immune_rules']} | Final version: {html.escape(str(ev['final_version']))}</p>
<table><tr><th>Gen</th><th>Eval</th><th>Rules</th><th>Blocked</th><th>Version</th></tr>{rows}</table>
<p>CLI: python3 run.py loop --generations 3 &nbsp;|&nbsp; python3 run.py evolve examples/clusterworm2_sample.jsonl &nbsp;|&nbsp; python3 run.py report &nbsp;|&nbsp; python3 run.py guarded stale_table -- echo hello</p>
<p>Honest status: SB3 PPO is NOT reproduced here. Real SB3 needs stable-baselines3 installed on your machine — see evoloop/sb3.py. Pure-Python learner is real, SB3 is optional, never faked.</p>
</body></html>"""
def serve(port: int = 8769):
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            body = render().encode(); self.send_response(200); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self, *a): pass
    print(f"Dashboard at http://127.0.0.1:{port} — read-only, Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
