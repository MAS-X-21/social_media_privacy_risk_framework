"""Report generation (Markdown and standalone HTML). Output is escaped."""
import html
from datetime import date
from .scoring import Assessment

COLORS = {"LOW": "#2e7d32", "MODERATE": "#f9a825", "HIGH": "#ef6c00", "CRITICAL": "#c62828"}

def to_markdown(a: Assessment, title: str = "Social Media Privacy Risk Report") -> str:
    L = [f"# {title}", f"_Generated {date.today().isoformat()} (synthetic or voluntarily entered demo data)_", "",
         f"## Overall: **{a.overall}/100 - {a.level}**",
         "(Higher score = higher exposure/risk.)", "",
         f"Base score {a.base_score} + compounding bonus {a.bonus}", "",
         "## Category scores", "", "| Category | Score |", "|---|---|"]
    from .questions import CATEGORY_BY_KEY
    for k, v in sorted(a.category_scores.items(), key=lambda kv: -kv[1]):
        L.append(f"| {CATEGORY_BY_KEY[k].name} | {v} |")
    if a.adjustments:
        L += ["", "## Compounding risks"] + [f"- **{x['title']}** (+{x['points']}): {x['explanation']}" for x in a.adjustments]
    L += ["", "## Detected weaknesses"]
    L += [f"- [{w['severity']}] **{w['category']}** - {w['finding']} (answer: {w['your_answer']})" for w in a.weaknesses] or ["- None detected."]
    L += ["", "## Prioritised recommendations"]
    L += [f"{r['rank']}. ({r['priority']}) **{r['category']}** - {r['action']}" for r in a.recommendations] or ["- Keep up the good habits."]
    L += ["", "## Privacy checklist"] + [f"- [{'x' if c['done'] else ' '}] {c['category']}: {c['item']}" for c in a.checklist]
    L += ["", "## Security-awareness guidance"] + [f"- **{g['category']}**: {g['guidance']}" for g in a.awareness]
    L += ["", "---", f"*{a.disclaimer}*"]
    return "\n".join(L)

def to_html(a: Assessment, title: str = "Social Media Privacy Risk Report") -> str:
    e = html.escape
    col = COLORS[a.level]
    from .questions import CATEGORY_BY_KEY
    bars = "".join(
        f"<div class='row'><span>{e(CATEGORY_BY_KEY[k].name)}</span><div class='bar'><i style='width:{v}%'></i></div><b>{v}</b></div>"
        for k, v in sorted(a.category_scores.items(), key=lambda kv: -kv[1]))
    weak = "".join(f"<li><b>[{e(w['severity'])}] {e(w['category'])}</b>: {e(w['finding'])}</li>" for w in a.weaknesses) or "<li>None detected.</li>"
    recs = "".join(f"<li><b>{e(r['priority'])}</b> - {e(r['category'])}: {e(r['action'])}</li>" for r in a.recommendations) or "<li>Keep up the good habits.</li>"
    chk = "".join(f"<li>{'&#9745;' if c['done'] else '&#9744;'} {e(c['category'])}: {e(c['item'])}</li>" for c in a.checklist)
    aw = "".join(f"<li><b>{e(g['category'])}</b>: {e(g['guidance'])}</li>" for g in a.awareness)
    adj = "".join(f"<li><b>{e(x['title'])}</b> (+{x['points']}): {e(x['explanation'])}</li>" for x in a.adjustments)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{{font-family:system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;color:#222}}
.score{{font-size:3rem;font-weight:700;color:{col}}}.row{{display:flex;gap:.6rem;align-items:center;margin:.25rem 0}}
.row span{{width:260px;font-size:.9rem}}.bar{{flex:1;background:#eee;height:12px;border-radius:6px}}
.bar i{{display:block;height:12px;border-radius:6px;background:{col}}}.note{{background:#fff8e1;padding:.8rem;border-radius:6px}}
li{{margin:.3rem 0}}</style></head><body>
<h1>{e(title)}</h1><div class="score">{a.overall}/100 - {e(a.level)}</div>
<p>Higher score = higher exposure/risk. Base {a.base_score} + compounding bonus {a.bonus}.</p>
<h2>Category scores</h2>{bars}
{"<h2>Compounding risks</h2><ul>"+adj+"</ul>" if adj else ""}
<h2>Detected weaknesses</h2><ul>{weak}</ul>
<h2>Recommendations</h2><ol>{recs}</ol>
<h2>Privacy checklist</h2><ul style="list-style:none;padding:0">{chk}</ul>
<h2>Security-awareness guidance</h2><ul>{aw}</ul>
<p class="note">{e(a.disclaimer)}</p></body></html>"""
