import re
import time
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

from src.crew import build_crew
from src.data.bangalore import BANGALORE_DATA, get_all_area_names, CITY_AVERAGES

load_dotenv()

st.set_page_config(
    page_title="PropSense AI",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Global CSS — light, clean, elegant
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    section[data-testid="stSidebar"] { display: none; }

    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 780px !important;
    }

    /* hero */
    .brand {
        text-align: center; margin-bottom: 2.5rem;
    }
    .brand h1 {
        font-size: 2.2rem; font-weight: 700; color: #111827;
        margin: 0; letter-spacing: -0.5px;
    }
    .brand p {
        color: #6b7280; font-size: 1rem; margin-top: 0.3rem;
    }


    /* verdict */
    .verdict-card {
        border-radius: 16px; padding: 2rem; text-align: center;
        margin: 1.5rem 0; color: white;
    }
    .verdict-good {
        background: linear-gradient(135deg, #059669, #34d399);
        box-shadow: 0 8px 30px rgba(5,150,105,0.2);
    }
    .verdict-risky {
        background: linear-gradient(135deg, #d97706, #fbbf24);
        box-shadow: 0 8px 30px rgba(217,119,6,0.2);
    }
    .verdict-avoid {
        background: linear-gradient(135deg, #dc2626, #f87171);
        box-shadow: 0 8px 30px rgba(220,38,38,0.2);
    }
    .v-score { font-size: 3rem; font-weight: 800; margin: 0; }
    .v-label {
        font-size: 1rem; font-weight: 600; letter-spacing: 2.5px;
        text-transform: uppercase; opacity: 0.95;
    }
    .v-summary {
        font-size: 0.95rem; margin-top: 0.7rem; opacity: 0.9;
        max-width: 600px; margin-left: auto; margin-right: auto;
    }

    /* stat pills */
    .stats-row { display: flex; gap: 0.6rem; margin: 1rem 0; }
    .stat {
        flex: 1; text-align: center; background: #f9fafb;
        border: 1px solid #f3f4f6; border-radius: 10px; padding: 0.7rem 0.4rem;
    }
    .stat-val { font-size: 1.15rem; font-weight: 700; color: #111827; }
    .stat-lbl {
        font-size: 0.65rem; color: #9ca3af; text-transform: uppercase;
        letter-spacing: 1px; margin-top: 0.1rem;
    }

    /* query badge */
    .q-badge {
        background: #eff6ff; border: 1px solid #dbeafe; border-radius: 10px;
        padding: 0.7rem 1rem; color: #1d4ed8; font-size: 0.88rem;
        margin-bottom: 1.2rem; line-height: 1.5;
    }

    /* section divider */
    .section-title {
        font-size: 0.7rem; font-weight: 600; color: #9ca3af;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin-top: 1.8rem; margin-bottom: 0.5rem;
    }

    /* how-it-works steps */
    .steps {
        display: flex; gap: 0.8rem; margin: 1rem 0 0.5rem 0;
    }
    .step {
        flex: 1; text-align: center; padding: 0.9rem 0.5rem;
        background: #f9fafb; border: 1px solid #f3f4f6;
        border-radius: 10px;
    }
    .step-icon { font-size: 1.5rem; }
    .step-name { font-size: 0.75rem; font-weight: 600; color: #374151; margin-top: 0.3rem; }
    .step-desc { font-size: 0.65rem; color: #9ca3af; }

    /* expander tweaks */
    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
    }

    /* hide streamlit branding */
    #MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_report(text: str) -> dict:
    r = {"score": None, "verdict": None, "summary": "", "sections": {}, "raw": str(text)}

    m = re.search(r"INVESTMENT SCORE:\s*([\d.]+)\s*/\s*10", text, re.I)
    if m:
        try:
            r["score"] = float(m.group(1))
        except ValueError:
            pass

    m = re.search(r"VERDICT:\s*(Good|Risky|Avoid)", text, re.I)
    if m:
        r["verdict"] = m.group(1).capitalize()

    m = re.search(r"Executive Summary\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL | re.I)
    if m:
        r["summary"] = m.group(1).strip()

    for name in [
        "Location Overview", "Price & Trend Analysis", "Rental & ROI Potential",
        "Buyer Sentiment & Livability", "Risk Factors",
        "Your Concerns Addressed", "Final Recommendation",
    ]:
        m = re.search(rf"##\s*{re.escape(name)}\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL | re.I)
        if m:
            r["sections"][name] = m.group(1).strip()
    return r


def make_map(area: str) -> folium.Map:
    c = BANGALORE_DATA[area]["coordinates"]
    m = folium.Map(location=c, zoom_start=13, tiles="CartoDB positron")
    for name, d in BANGALORE_DATA.items():
        sel = name == area
        folium.CircleMarker(
            location=d["coordinates"],
            radius=14 if sel else 5,
            tooltip=name,
            popup=folium.Popup(
                f"<b>{name}</b><br>₹{d['price_per_sqft']['avg']:,}/sqft &bull; {d['trend_pct']}",
                max_width=200,
            ),
            color="#ef4444" if sel else "#d1d5db",
            fill=True,
            fill_color="#ef4444" if sel else "#e5e7eb",
            fill_opacity=0.9 if sel else 0.4,
            weight=3 if sel else 1,
        ).add_to(m)
    return m


# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------
has_report = "last_report" in st.session_state


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  LANDING PAGE                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝
if not has_report:

    st.markdown("""
    <div class="brand">
        <h1>🏠 PropSense AI</h1>
        <p>Should you invest in that Bangalore locality? Let AI agents find out.</p>
    </div>
    """, unsafe_allow_html=True)

    location = st.selectbox("Location", get_all_area_names(), label_visibility="collapsed")
    budget = st.slider("Budget (₹ Lakhs)", 10, 500, 80, step=10)
    if budget >= 100:
        st.caption(f"₹{budget / 100:.1f} Crore")

    user_query = st.text_area(
        "What are you looking for?",
        placeholder=(
            "e.g. I'm a 28-year-old software engineer. Looking for a 2BHK "
            "for rental income, plan to hold 5 years. Worried about traffic "
            "and water supply..."
        ),
        height=110,
        label_visibility="collapsed",
    )

    analyze = st.button("Analyze Investment →", use_container_width=True, type="primary")

    # --- how it works ---
    st.markdown("""
    <div class="steps">
        <div class="step"><div class="step-icon">🧠</div><div class="step-name">Research</div><div class="step-desc">Market data</div></div>
        <div class="step"><div class="step-icon">📊</div><div class="step-name">Analyze</div><div class="step-desc">Price & ROI</div></div>
        <div class="step"><div class="step-icon">🔎</div><div class="step-name">Investigate</div><div class="step-desc">Ground reality</div></div>
        <div class="step"><div class="step-icon">📋</div><div class="step-name">Report</div><div class="step-desc">Your verdict</div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- trigger ---
    if analyze:
        if not user_query.strip():
            st.warning("Please describe what you're looking for.")
            st.stop()

        AGENTS = [
            ("🧠", "Researcher", "Collecting market data for " + location),
            ("📊", "Analyst", "Crunching pricing, ROI & budget fit"),
            ("🔎", "Investigator", "Checking ground reality & risks"),
            ("📋", "Reporter", "Writing your personalized verdict"),
        ]

        st.markdown("---")
        progress_bar = st.progress(0, text="Starting analysis...")
        step_slots = [st.empty() for _ in AGENTS]
        counter = {"done": 0}

        def _render_steps():
            for i, (icon, name, desc) in enumerate(AGENTS):
                if i < counter["done"]:
                    step_slots[i].markdown(
                        f"&ensp; ✅ &ensp; **{name}** — Done"
                    )
                elif i == counter["done"]:
                    step_slots[i].markdown(
                        f"&ensp; ⏳ &ensp; **{name}** — *{desc}...*"
                    )
                else:
                    step_slots[i].markdown(
                        f"&ensp; ⬜ &ensp; {name}"
                    )
            pct = int(counter["done"] / len(AGENTS) * 100)
            label = AGENTS[min(counter["done"], len(AGENTS) - 1)][1]
            progress_bar.progress(
                max(pct, 5),
                text=f"Agent {counter['done'] + 1}/4 — {label} is working..."
                if counter["done"] < 4
                else "All agents finished!",
            )

        def on_task_done(_output):
            counter["done"] += 1
            _render_steps()

        _render_steps()

        try:
            crew = build_crew(location, budget, user_query, task_callback=on_task_done)
            result = crew.kickoff()
            counter["done"] = 4
            _render_steps()
            progress_bar.progress(100, text="✅ Analysis complete!")
        except Exception as e:
            progress_bar.progress(100, text="❌ Analysis failed")
            st.error(f"Agent error: {e}")
            st.stop()

        st.session_state["last_report"] = str(result)
        st.session_state["last_location"] = location
        st.session_state["last_budget"] = budget
        st.session_state["last_query"] = user_query
        time.sleep(1)
        st.rerun()


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS PAGE                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝
if has_report:
    loc = st.session_state["last_location"]
    bgt = st.session_state["last_budget"]
    query = st.session_state.get("last_query", "")
    report = parse_report(st.session_state["last_report"])
    d = BANGALORE_DATA[loc]
    bgt_str = f"₹{bgt / 100:.1f} Cr" if bgt >= 100 else f"₹{bgt:.0f}L"

    # --- header ---
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"""
        <div class="brand" style="text-align:left">
            <h1>{loc}</h1>
            <p>Budget {bgt_str} &bull; {d['locality_vibe']}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("")
        if st.button("← Back"):
            for k in ["last_report", "last_location", "last_budget", "last_query"]:
                st.session_state.pop(k, None)
            st.rerun()

    if query:
        st.markdown(f'<div class="q-badge">💬 &nbsp;{query}</div>', unsafe_allow_html=True)

    # --- verdict ---
    if report["score"] is not None and report["verdict"]:
        css = {"Good": "verdict-good", "Risky": "verdict-risky", "Avoid": "verdict-avoid"}.get(
            report["verdict"], "verdict-risky"
        )
        emoji = {"Good": "✅", "Risky": "⚠️", "Avoid": "❌"}.get(report["verdict"], "")
        st.markdown(f"""
        <div class="verdict-card {css}">
            <div class="v-score">{report['score']}/10</div>
            <div class="v-label">{emoji} {report['verdict']}</div>
            <div class="v-summary">{report['summary'][:280]}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- stats ---
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat"><div class="stat-val">₹{d['price_per_sqft']['avg']:,}</div><div class="stat-lbl">Avg ₹/sqft</div></div>
        <div class="stat"><div class="stat-val">{d['trend_pct']}</div><div class="stat-lbl">YoY Growth</div></div>
        <div class="stat"><div class="stat-val">{d['rental_yield']}%</div><div class="stat-lbl">Rental Yield</div></div>
        <div class="stat"><div class="stat-val">{d['buyer_sentiment_score']}/10</div><div class="stat-lbl">Sentiment</div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- map ---
    st.markdown('<div class="section-title">Location Map</div>', unsafe_allow_html=True)
    st_folium(make_map(loc), width=None, height=340, returned_objects=[])

    # --- report sections ---
    icons = {
        "Location Overview": "📍", "Price & Trend Analysis": "💰",
        "Rental & ROI Potential": "📈", "Buyer Sentiment & Livability": "💬",
        "Risk Factors": "⚠️", "Your Concerns Addressed": "💡",
        "Final Recommendation": "🎯",
    }

    st.markdown('<div class="section-title">Detailed Report</div>', unsafe_allow_html=True)

    for name, content in report["sections"].items():
        icon = icons.get(name, "📌")
        expanded = name in ("Final Recommendation", "Your Concerns Addressed")
        with st.expander(f"{icon}  {name}", expanded=expanded):
            st.markdown(content)

    with st.expander("📄  Raw Report"):
        st.markdown(report["raw"])
