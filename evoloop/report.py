"""Static HTML evolution report, no animation, no login. One page per evolve run."""
def render_report(data, path):
    rows = "".join(f"<tr><td>{g['generation']}</td><td>{g['eval']}</td><td>{g['immune_rules']}</td><td>{g['blocked']}</td><td>{g['version']}</td></tr>" for g in data.get("generations", []))
    html = f"""<!doctype html><html><head><meta charset=utf-8><title>EVOLVELOOP Report</title><style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}</style></head>
<body><h1>EVOLVELOOP — Evolution Report</h1><p>Immune rules: {data.get('final_immune_rules')} | Final version: {data.get('final_version')}</p>
<table><tr><th>Gen</th><th>Eval</th><th>Rules</th><th>Blocked</th><th>Version</th></tr>{rows}</table>
<p>Static page, no animation. Verify with: python3 run.py loop --generations 3</p></body></html>"""
    open(path, "w").write(html); return path
