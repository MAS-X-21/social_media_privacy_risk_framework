import os, sys, random, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from smprf.questions import QUESTIONS, CATEGORIES
from smprf.scoring import assess, risk_level, validate_answers
from smprf.synthetic import generate_profiles, synthetic_answers
from smprf.report import to_html, to_markdown
from smprf.dashboard import build_dashboard

def all_with(risk_picker):
    a = {}
    for q in QUESTIONS:
        a[q.id] = risk_picker(q)
    return a

best = lambda q: min(range(len(q.options)), key=lambda i: q.options[i][1])
worst = lambda q: max(range(len(q.options)), key=lambda i: q.options[i][1])

class Tests(unittest.TestCase):
    def test_bank_shape(self):
        self.assertEqual(len(CATEGORIES), 20)
        self.assertEqual(len(QUESTIONS), 40)

    def test_best_is_low_worst_is_critical(self):
        lo, hi = assess(all_with(best)), assess(all_with(worst))
        self.assertEqual(lo.overall, 0); self.assertEqual(lo.level, "LOW")
        self.assertEqual(hi.overall, 100); self.assertEqual(hi.level, "CRITICAL")

    def test_level_boundaries(self):
        for s, lvl in [(0,"LOW"),(20,"LOW"),(21,"MODERATE"),(40,"MODERATE"),(41,"HIGH"),(70,"HIGH"),(71,"CRITICAL"),(100,"CRITICAL")]:
            self.assertEqual(risk_level(s), lvl, s)

    def test_higher_risk_never_lowers_score(self):
        base = all_with(best)
        prev = assess(base).overall
        for q in QUESTIONS:
            base[q.id] = worst(q)
            cur = assess(base).overall
            self.assertGreaterEqual(cur, prev)
            prev = cur

    def test_bonus_cap_and_range(self):
        a = assess(all_with(worst))
        self.assertLessEqual(a.bonus, 15)
        self.assertTrue(0 <= a.overall <= 100)

    def test_compounding_rule_fires(self):
        a = all_with(best); a["mf1"] = worst([q for q in QUESTIONS if q.id=="mf1"][0]); a["pr1"] = 4
        res = assess(a)
        self.assertIn("R1", [x["id"] for x in res.adjustments])

    def test_validation(self):
        with self.assertRaises(ValueError): validate_answers({"nope": 0})
        with self.assertRaises(ValueError): validate_answers({"pv1": 99})
        with self.assertRaises(ValueError): assess({})

    def test_partial_answers(self):
        res = assess({"mf1": 3})
        self.assertEqual(res.answered, 1)

    def test_synthetic_deterministic_and_ordered(self):
        self.assertEqual(generate_profiles(20, 7), generate_profiles(20, 7))
        rng = random.Random(3)
        avg = lambda p: sum(assess(synthetic_answers(p, rng)).overall for _ in range(30)) / 30
        self.assertGreater(avg("careless"), avg("average"))
        self.assertGreater(avg("average"), avg("aware"))
        self.assertGreater(avg("aware"), avg("hardened"))

    def test_reports_escape_and_render(self):
        res = assess(all_with(worst))
        self.assertIn("CRITICAL", to_markdown(res)); self.assertIn("<html", to_html(res))
        self.assertIn("synthetic", build_dashboard(generate_profiles(10)).lower())

if __name__ == "__main__":
    unittest.main()
