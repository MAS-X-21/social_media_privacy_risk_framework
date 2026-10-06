"""Command-line interface. Run: python -m smprf --help"""
import argparse
import json
import os
import random
import sys
from .questions import CATEGORIES, QUESTIONS
from .scoring import assess
from .synthetic import PERSONAS, generate_profiles, synthetic_answers, write_csv
from .report import to_html, to_markdown
from .dashboard import build_dashboard

def _print_result(a):
    from .questions import CATEGORY_BY_KEY
    print(f"\n=== PRIVACY RISK SCORE: {a.overall}/100  [{a.level}] ===")
    print("(Higher = more exposure. Educational framework, not a guarantee.)\n")
    for k, v in sorted(a.category_scores.items(), key=lambda kv: -kv[1]):
        print(f"  {CATEGORY_BY_KEY[k].name:<38}{v:>6.1f}  {'#' * int(v / 5)}")
    print("\nTop recommendations:")
    for r in a.recommendations[:5]:
        print(f"  {r['rank']}. [{r['priority']}] {r['category']}: {r['action']}")
    print(f"\n{a.disclaimer}")

def _save(a, out_dir, stem):
    os.makedirs(out_dir, exist_ok=True)
    md = os.path.join(out_dir, stem + ".md"); ht = os.path.join(out_dir, stem + ".html")
    open(md, "w", encoding="utf-8").write(to_markdown(a))
    open(ht, "w", encoding="utf-8").write(to_html(a))
    print(f"\nReports saved: {md} and {ht}")

def cmd_assess(args):
    print("Social Media Privacy Risk Assessment - answer about YOUR OWN settings (or a fictional persona).")
    print("Nothing is sent anywhere; no accounts are accessed.\n")
    answers = {}
    for c in CATEGORIES:
        print(f"\n--- {c.name}: {c.description}")
        for q in [x for x in QUESTIONS if x.category == c.key]:
            print(f"\n{q.text}")
            for i, (lab, _) in enumerate(q.options, 1):
                print(f"  {i}. {lab}")
            while True:
                raw = input("Choose number: ").strip()
                if raw.isdigit() and 1 <= int(raw) <= len(q.options):
                    answers[q.id] = int(raw) - 1
                    break
                print("Invalid choice, try again.")
    a = assess(answers)
    _print_result(a)
    if args.report:
        _save(a, args.out, "my_report")

def cmd_demo(args):
    rng = random.Random(args.seed)
    a = assess(synthetic_answers(args.persona, rng))
    print(f"[Synthetic persona: {args.persona}]")
    _print_result(a)
    if args.report:
        _save(a, args.out, f"demo_{args.persona}")

def cmd_file(args):
    with open(args.path, encoding="utf-8") as f:
        answers = json.load(f)
    a = assess(answers)
    _print_result(a)
    if args.report:
        _save(a, args.out, "file_report")

def cmd_dashboard(args):
    rows = generate_profiles(args.n, args.seed)
    os.makedirs(args.out, exist_ok=True)
    csv_path = os.path.join(args.out, "synthetic_profiles.csv")
    html_path = os.path.join(args.out, "dashboard.html")
    write_csv(rows, csv_path)
    open(html_path, "w", encoding="utf-8").write(build_dashboard(rows))
    print(f"Generated {len(rows)} synthetic profiles.\nCSV: {csv_path}\nDashboard: {html_path}")

def main(argv=None):
    p = argparse.ArgumentParser(prog="smprf", description="Social Media Privacy Risk Assessment Framework (educational, defensive).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("assess", help="interactive questionnaire"); s.add_argument("--report", action="store_true"); s.add_argument("--out", default="reports"); s.set_defaults(fn=cmd_assess)
    s = sub.add_parser("demo", help="score a synthetic persona"); s.add_argument("--persona", choices=list(PERSONAS), default="average"); s.add_argument("--seed", type=int, default=1); s.add_argument("--report", action="store_true"); s.add_argument("--out", default="reports"); s.set_defaults(fn=cmd_demo)
    s = sub.add_parser("file", help="score answers from a JSON file {question_id: option_index}"); s.add_argument("path"); s.add_argument("--report", action="store_true"); s.add_argument("--out", default="reports"); s.set_defaults(fn=cmd_file)
    s = sub.add_parser("dashboard", help="generate synthetic dataset + HTML dashboard"); s.add_argument("--n", type=int, default=200); s.add_argument("--seed", type=int, default=42); s.add_argument("--out", default="reports"); s.set_defaults(fn=cmd_dashboard)
    args = p.parse_args(argv)
    args.fn(args)

if __name__ == "__main__":
    main()
