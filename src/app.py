"""
ModernizeIQ Dashboard — Streamlit frontend.

Reads the precomputed portfolio from data/results.json (instant, demo-safe) and
renders the portfolio view: risk scores, 6R decisions, retrieved patterns, and
plain-English explanations. Matches the dark slate + purple theme of the static mock.

Run:
    uv run streamlit run src/app.py
"""

import os
import sys
import json

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_MODEL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_PATH = os.path.join(ROOT,"data", "results.json")
APPS_PATH = os.path.join(ROOT, "data", "synthetic_apps.json")

st.set_page_config(page_title="ModernizeIQ", page_icon="🧭", layout="wide")

# ----------------------------------------------------------------------------- 
# Theme — dark slate + purple accent, JetBrains Mono for numbers
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #0b0f19; color: #f1f5f9; }
[data-testid="stHeader"] { background: #0b0f19; }
.metric-card {
  background: rgba(20, 26, 46, 0.8); border: 1px solid #334155;
  border-radius: 12px; padding: 16px 20px; text-align: center;
}
.metric-card .value { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; color: #f1f5f9; }
.metric-card .label { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: .08em; }
.decision-badge {
  display: inline-block; padding: 3px 12px; border-radius: 999px;
  font-size: 12px; font-weight: 600; letter-spacing: .03em;
}
.app-card {
  background: rgba(15, 23, 42, 0.65); border: 1px solid #334155;
  border-radius: 12px; padding: 18px 22px; margin-bottom: 14px;
}
.kb-chip {
  display: inline-block; background: #1e1b4b; color: #c4b5fd; border: 1px solid #4c1d95;
  border-radius: 6px; padding: 2px 8px; font-size: 11px; font-family: 'JetBrains Mono', monospace;
  margin-right: 6px; margin-top: 4px;
}
h1, h2, h3 { color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

DECISION_COLORS = {
    "Retire":     ("#7f1d1d", "#fca5a5"),
    "Replace":    ("#7c2d12", "#fdba74"),
    "Refactor":   ("#713f12", "#fde047"),
    "Replatform": ("#1e3a8a", "#93c5fd"),
    "Rehost":     ("#064e3b", "#6ee7b7"),
    "Retain":     ("#14532d", "#86efac"),
}

def badge(decision: str) -> str:
    bg, fg = DECISION_COLORS.get(decision, ("#334155", "#cbd5e1"))
    return f'<span class="decision-badge" style="background:{bg};color:{fg}">{decision}</span>'

def risk_color(score: int) -> str:
    if score >= 80: return "#f87171"
    if score >= 60: return "#fb923c"
    if score >= 40: return "#facc15"
    if score >= 20: return "#a3e635"
    return "#4ade80"

# ----------------------------------------------------------------------------- 
# Load results  (this section stays where it is)
# -----------------------------------------------------------------------------
if not os.path.exists(RESULTS_PATH):
    st.warning("No results yet. Run the batch pipeline first:  `uv run src/run_all.py`")
    st.stop()

with open(RESULTS_PATH) as f:
    payload = json.load(f)

meta = payload["meta"]
results = payload["results"]

# ----------------------------------------------------------------------------- 
# Header  (moved here — meta now exists)
# -----------------------------------------------------------------------------
st.markdown(
    "<h1 style='margin-bottom:0'>🧭 ModernizeIQ</h1>"
    "<p style='color:#94a3b8;margin-top:4px'>AI-powered application modernization advisor "
    "&nbsp;·&nbsp; TCS × AMD AI Hackathon &nbsp;·&nbsp; "
    f"<span style='font-family:JetBrains Mono,monospace'>{meta['model']}</span></p>",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------- 
# Portfolio metrics row
# -----------------------------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, str(meta["total_apps"]), "Applications"),
    (c2, f"{meta['accuracy_pct']}%", "Match vs golden labels"),
    (c3, str(sum(1 for r in results if r['risk_score'] >= 80)), "Critical risk (80+)"),
    (c4, str(sum(1 for r in results if r['decision'] == 'Retire')), "Retire candidates"),
    (c5, f"{meta.get('avg_latency_seconds') or '—'}s", "Avg latency / app"),
]
for col, value, label in cards:
    col.markdown(
        f'<div class="metric-card"><div class="value">{value}</div>'
        f'<div class="label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------- 
# Decision filter + portfolio table
# -----------------------------------------------------------------------------
decisions_present = sorted({r["decision"] for r in results})
selected = st.multiselect("Filter by decision", decisions_present, default=decisions_present)

filtered = [r for r in results if r["decision"] in selected]
filtered.sort(key=lambda r: -r["risk_score"])

st.markdown("### Portfolio")

for r in filtered:
    rc = risk_color(r["risk_score"])
    match_icon = "✅" if r.get("matches_expected") else "⚠️"
    kb_chips = "".join(f'<span class="kb-chip">{src}</span>' for src in r.get("retrieved_patterns", []))

    with st.container():
        st.markdown(
            f"""<div class="app-card">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap">
              <div>
                <span style="font-size:17px;font-weight:700">{r['app_name']}</span>
                &nbsp;{badge(r['decision'])}
                <span style="color:#64748b;font-size:12px">&nbsp;expected: {r.get('expected_6r')} {match_icon}</span>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:{rc}">
                {r['risk_score']}<span style="font-size:12px;color:#64748b">/100</span>
              </div>
            </div>
            <div style="color:#cbd5e1;font-size:14px;margin-top:8px">{r['headline']}</div>
            <div style="margin-top:6px">{kb_chips}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        with st.expander(f"Full analysis — {r['app_name']}"):
            colA, colB = st.columns(2)
            with colA:
                st.markdown("**Key risk factors**")
                for f_ in r["key_risk_factors"]:
                    st.markdown(f"- {f_}")
                st.markdown(f"**Confidence:** {r['confidence']}")
                st.markdown(f"**Assessment:** {r['assessment_summary']}")
            with colB:
                st.markdown("**Decision reasoning (grounded in retrieved patterns)**")
                st.markdown(r["decision_reasoning"])
            st.markdown("**Executive explanation**")
            st.info(r["explanation"])
            st.markdown(f"**Caveats:** {r['caveats']}")

# ----------------------------------------------------------------------------- 
# Footer
# -----------------------------------------------------------------------------
st.markdown(
    f"<p style='color:#475569;font-size:12px;margin-top:24px'>"
    f"Generated {meta['generated_at']} · model {meta['model']} · "
    f"{meta['succeeded']}/{meta['total_apps']} apps analyzed · synthetic data only</p>",
    unsafe_allow_html=True,
)