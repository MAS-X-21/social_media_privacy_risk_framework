"""Static HTML dashboard for AGGREGATE synthetic data (no JS, no network)."""
import html
from collections import Counter
from statistics import mean
from typing import List
from .questions import CATEGORIES
from .report import COLORS

def build_dashboard(rows: List[dict], title="Synthetic Privacy Risk Dashboard") -> str:
    e = html.escape
    n = len(rows)
    lv = Counter(r["level"] for r in rows)
    avg = mean(r["score"] for r in rows)
    cards = "".join(f"<div class='card' style='border-top:5px solid {COLORS[l]}'><b>{lv.get(l,0)}</b><br>{l}<br><small>{100*lv.get(l,0)/n:.0f}%</small></div>"
                    for l in ["LOW", "MODERATE", "HIGH", "CRITICAL"])
    cat = sorted(((c.name, mean(r[c.key] for r in rows)) for c in CATEGORIES), key=lambda x: -x[1])
    cat_bars = "".join(f"<div class='row'><span>{e(nm)}</span><div class='bar'><i style='width:{v:.0f}%'></i></div><b>{v:.0f}</b></div>" for nm, v in cat)
    personas = sorted({r["persona"] for r in rows})
    p_rows = "".join(f"<tr><td>{e(p)}</td><td>{sum(1 for r in rows if r['persona']==p)}</td><td>{mean(r['score'] for r in rows if r['persona']==p):.1f}</td></tr>" for p in personas)
    bins = [0] * 10
    for r in rows:
        bins[min(9, r["score"] // 10)] += 1
    mx = max(bins) or 1
    hist = "".join(f"<div class='col'><i style='height:{100*b/mx:.0f}px'></i><small>{i*10}-{i*10+9}</small><small>{b}</small></div>" for i, b in enumerate(bins))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#222}}
.cards{{display:flex;gap:1rem;flex-wrap:wrap}}.card{{flex:1;min-width:130px;padding:1rem;background:#f6f6f6;border-radius:8px;text-align:center}}
.card b{{font-size:1.8rem}}.row{{display:flex;gap:.6rem;align-items:center;margin:.2rem 0}}.row span{{width:270px;font-size:.85rem}}
.bar{{flex:1;background:#eee;height:12px;border-radius:6px}}.bar i{{display:block;height:12px;border-radius:6px;background:#5c6bc0}}
.hist{{display:flex;gap:6px;align-items:flex-end;height:150px}}.col{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}}
.col i{{width:100%;background:#5c6bc0;display:block;border-radius:3px 3px 0 0}}table{{border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:.4rem .8rem}}
.note{{background:#fff8e1;padding:.8rem;border-radius:6px}}</style></head><body>
<h1>{e(title)}</h1>
<p class="note">All data is <b>synthetic/fictional</b> ({n} generated profiles). No real individuals are represented. Higher score = higher exposure.</p>
<h2>Average score: {avg:.1f}/100</h2><div class="cards">{cards}</div>
<h2>Score distribution</h2><div class="hist">{hist}</div>
<h2>Average category risk (highest first)</h2>{cat_bars}
<h2>By persona</h2><table><tr><th>Persona</th><th>Profiles</th><th>Avg score</th></tr>{p_rows}</table>
</body></html>"""
