"""Optional Streamlit web UI.  Run:  streamlit run app.py
Requires: pip install streamlit pandas   (core framework itself needs only the standard library)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import streamlit as st
import pandas as pd
from smprf.questions import CATEGORIES, QUESTIONS, CATEGORY_BY_KEY
from smprf.scoring import assess
from smprf.synthetic import generate_profiles
from smprf.report import to_markdown, to_html

st.set_page_config(page_title="Social Media Privacy Risk Framework", page_icon="🛡️", layout="wide")
st.title("🛡️ Social Media Privacy Risk Assessment Framework")
st.caption("Educational, defensive tool. Uses only answers YOU enter. No scraping, no real-profile lookups. Higher score = higher exposure.")

page = st.sidebar.radio("Page", ["Assessment", "Synthetic dashboard", "About"])

if page == "Assessment":
    answers = {}
    with st.form("assessment"):
        for c in CATEGORIES:
            with st.expander(f"{c.name} - {c.description}"):
                for q in [x for x in QUESTIONS if x.category == c.key]:
                    labels = [o[0] for o in q.options]
                    answers[q.id] = labels.index(st.radio(q.text, labels, key=q.id, index=0))
        submitted = st.form_submit_button("Calculate my privacy risk")
    if submitted:
        a = assess(answers)
        st.metric("Privacy Risk Score (0-100)", f"{a.overall}", a.level, delta_color="off")
        st.subheader("Category scores")
        df = pd.DataFrame({"Category": [CATEGORY_BY_KEY[k].name for k in a.category_scores],
                           "Score": list(a.category_scores.values())}).sort_values("Score", ascending=False)
        st.bar_chart(df.set_index("Category"))
        st.subheader("Detected weaknesses")
        for w in a.weaknesses:
            st.warning(f"**[{w['severity']}] {w['category']}** - {w['finding']}")
        st.subheader("Recommendations")
        for r in a.recommendations:
            st.write(f"{r['rank']}. **{r['priority']}** - {r['category']}: {r['action']}")
        st.subheader("Checklist")
        for c in a.checklist:
            st.checkbox(f"{c['category']}: {c['item']}", value=c["done"], disabled=True)
        st.subheader("Awareness guidance")
        for g in a.awareness:
            st.info(f"**{g['category']}**: {g['guidance']}")
        st.download_button("Download report (HTML)", to_html(a), "privacy_report.html", "text/html")
        st.download_button("Download report (Markdown)", to_markdown(a), "privacy_report.md")
        st.caption(a.disclaimer)

elif page == "Synthetic dashboard":
    n = st.sidebar.slider("Synthetic profiles", 50, 1000, 200, 50)
    seed = st.sidebar.number_input("Seed", value=42)
    df = pd.DataFrame(generate_profiles(n, int(seed)))
    st.info("All profiles are fictional (DEMO-xxxx).")
    c1, c2 = st.columns(2)
    c1.metric("Average score", f"{df.score.mean():.1f}")
    c2.metric("CRITICAL share", f"{(df.level == 'CRITICAL').mean() * 100:.0f}%")
    st.bar_chart(df.level.value_counts().reindex(["LOW", "MODERATE", "HIGH", "CRITICAL"]).fillna(0))
    st.bar_chart(df[[c.key for c in CATEGORIES]].mean().sort_values(ascending=False))
    st.bar_chart(df.groupby("persona").score.mean())
    st.dataframe(df)

else:
    st.markdown("""
**Risk levels:** 0-20 LOW · 21-40 MODERATE · 41-70 HIGH · 71-100 CRITICAL.

This is an educational risk framework, **not a guarantee** an account will or will not be compromised.
See `docs/methodology.md` for scoring details and `docs/ethics_and_scope.md` for boundaries.
""")
