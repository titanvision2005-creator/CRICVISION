import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
from PIL import Image

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Opponent Analysis | CricVision",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# PALETTE 1 CSS (HIGH CONTRAST & CARD SCOPING)
# =====================================

st.markdown("""
<style>

/* Hide default Streamlit chrome */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1200px;
}

/* Sidebar: Palette 1 Obsidian */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B0F19, #111827) !important;
    border-right: 2px solid #0284C7 !important;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Canvas Background */
.stApp {
    background-color: #E5E4E0 !important;
    color: #0F172A;
}

.main .block-container {
    background: transparent;
}

/* Page Outer Section Titles (on Alabaster Canvas) */
h1.page-title, h2.page-title, h3.page-title {
    color: #0F172A !important;
    font-weight: 900 !important;
    letter-spacing: 0.3px;
}

/* =========================
   SELECTBOX / SEARCH BAR FIX
========================= */

div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label p {
    color: #0F172A !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1.5px solid #0284C7 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
}

div[data-baseweb="select"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-baseweb="select"] svg {
    fill: #0284C7 !important;
}

/* Dropdown popover and list */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #111827 !important;
    border: 1px solid #0284C7 !important;
    border-radius: 12px !important;
}

ul[role="listbox"] li,
div[data-baseweb="menu"] * {
    color: #F8FAFC !important;
    background-color: #111827 !important;
}

ul[role="listbox"] li:hover,
div[data-baseweb="menu"] li:hover,
li[aria-selected="true"] {
    background-color: #1E293B !important;
    color: #38BDF8 !important;
}

/* =========================
   BUTTON STYLING
========================= */

.stButton button {
    width: 100%;
    height: 48px;
    background: #0284C7 !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 14px !important;
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35) !important;
    transition: 0.3s !important;
}

.stButton button:hover {
    background: #0369A1 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(2, 132, 199, 0.50) !important;
}

/* =========================
   MATCH TITLE BANNER
========================= */

.match-banner {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    border-radius: 18px;
    padding: 20px 24px;
    border: 1.5px solid #0284C7;
    margin: 22px 0 25px 0;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    text-align: center;
}

.match-banner h2 {
    color: #38BDF8 !important;
    margin: 0 !important;
    font-size: 24px !important;
    font-weight: 900 !important;
}

/* =========================
   KPI METRIC CARDS FIX (HIGH CONTRAST)
========================= */

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%) !important;
    padding: 20px !important;
    border-radius: 18px !important;
    border: 1px solid #334155 !important;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18) !important;
}

[data-testid="stMetric"] * {
    color: #FFFFFF !important;
}

[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #CBD5E1 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div {
    color: #38BDF8 !important;
    font-size: 32px !important;
    font-weight: 900 !important;
}

/* =========================
   INFO & RECOMMENDATION CARDS
========================= */

.info-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #334155;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    transition: 0.3s;
    margin-bottom: 12px;
}

.info-card:hover {
    transform: translateY(-4px);
    border-color: #0284C7;
    box-shadow: 0 14px 30px rgba(2, 132, 199, 0.28);
}

.info-card h3, .info-card h4 {
    color: #38BDF8 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin-top: 0 !important;
    margin-bottom: 14px !important;
}

.info-card p {
    color: #E2E8F0 !important;
    font-size: 14.5px !important;
    line-height: 1.8 !important;
    margin-bottom: 8px !important;
}

.info-card b {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* =========================
   STATUS ALERTS (INSIGHTS)
========================= */

div[data-testid="stAlert"] {
    background-color: #111827 !important;
    border-radius: 14px !important;
    border: 1.5px solid #0284C7 !important;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15) !important;
}

div[data-testid="stAlert"] * {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

hr {
    border-color: #CBD5E1 !important;
}

.stProgress > div > div > div > div {
    background-color: #0284C7 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# LOAD WIDE BANNER LOGO
# =====================================

def get_base64_banner():
    candidate_paths = [
        "logo.png",
        "Picsart_26-10-31_19-37-06-915.png",
        "banner.png",
        "cricvision_banner.png",
        "[logo].png"
    ]
    all_paths = []
    for p in candidate_paths:
        all_paths.append(p)
        all_paths.append(os.path.join("..", p))

    for path in all_paths:
        if os.path.exists(path):
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    if w / h > 1.3:
                        with open(path, "rb") as f:
                            return base64.b64encode(f.read()).decode()
            except Exception:
                continue

    for path in all_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                continue
    return ""

banner_logo = get_base64_banner()


# =====================================
# HEADER
# =====================================

if banner_logo:
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 15px 0;">
        <img src="data:image/png;base64,{banner_logo}" style="width:100%; max-width:620px; height:auto; border-radius:12px;">
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom: 25px;">
    <h1 style="font-size:38px; font-weight:900; color:#0F172A; margin:0 0 6px 0;">
    ⚔️ Opponent Intelligence Module
    </h1>
    <p style="font-size:16px; color:#475569; margin:0;">
    Analyze Head-to-Head Tactical Records, Innings Ceilings & Venue Splits
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================
# LOAD DATA (DYNAMIC FILE CHECK)
# =====================================

@st.cache_data
def load_opponent_data():
    candidate_paths = [
        "TITAN VISION.xlsx",
        os.path.join("..", "TITAN VISION.xlsx")
    ]
    excel_path = None
    for p in candidate_paths:
        if os.path.exists(p):
            excel_path = p
            break
            
    if not excel_path:
        raise FileNotFoundError("TITAN VISION.xlsx not found.")

    df = pd.read_excel(excel_path, sheet_name="OPPONENT_DATA")
    df.columns = df.columns.astype(str).str.strip()
    return df

try:
    df = load_opponent_data()
except Exception as e:
    st.error(f"Unable to load Excel dataset: {e}")
    st.stop()


# =====================================
# FILTERS
# =====================================

c1, c2 = st.columns(2)

with c1:
    team_list = sorted(df["OPPONENT"].dropna().unique().tolist())
    team1 = st.selectbox(
        "Select Opponent",
        team_list,
        index=None,
        placeholder="Choose Opponent"
    )

with c2:
    # Filter out OVERALL so only physical stadiums are selectable
    venue_list = sorted([
        v for v in df["VENUE"].dropna().unique().tolist() 
        if str(v).strip().upper() != "OVERALL"
    ])
    venue = st.selectbox(
        "Select Venue",
        venue_list,
        index=None,
        placeholder="Choose Venue (or leave empty for Overall)"
    )

Analyze = st.button("🚀 Generate Analysis")

if Analyze and team1 is None:
    st.warning("Please select an opponent to generate the analysis.")
    st.stop()

# =====================================
# MAIN LOGIC
# =====================================

if Analyze:

    if venue is None:
        filtered = df[
            (df["OPPONENT"] == team1) &
            (df["VENUE"].astype(str).str.strip().str.upper() == "OVERALL")
        ]
        venue_label = "Overall Records"
    else:
        filtered = df[
            (df["OPPONENT"] == team1) &
            (df["VENUE"] == venue)
        ]
        venue_label = venue

    if filtered.empty:
        st.warning(f"No head-to-head match records found for {team1} at {venue_label}.")
        st.stop()

    row = filtered.iloc[0]

    # Resolve focus team columns dynamically
    def get_val(df_row, primary_col, fallback_col):
        if primary_col in df_row.index and pd.notna(df_row[primary_col]):
            return df_row[primary_col]
        if fallback_col in df_row.index and pd.notna(df_row[fallback_col]):
            return df_row[fallback_col]
        return 0

    matches = row.get("MATCHES", 0)
    win = row.get("WINS", 0)
    lose = row.get("LOSSES", 0)

    winp = float(row.get("WIN%", 0))
    losep = float(row.get("LOSE%", 0))

    high = get_val(row, "HIGHEST GT SCORE", "HIGHEST SCORE")
    low = get_val(row, "LOWEST GT SCORE", "LOWEST SCORE")
    avg = float(get_val(row, "AVERAGE GT SCORE", "AVERAGE SCORE"))
    avgwkts = get_val(row, "AVERAGE GT WICKETS", "AVERAGE WICKETS")
    avgovers = get_val(row, "AVERAGE GT OVERS", "AVERAGE OVERS")

    high1 = row.get("HIGHEST OPPONENT SCORE", 0)
    low1 = row.get("LOWEST OPPONENT SCORE", 0)
    avg1 = float(row.get("AVERAGE OPPONENT SCORE", 0))
    avg2 = row.get("AVERAGE OPPONENT WICKETS TAKEN", 0)
    avg3 = row.get("AVERAGE OPPONENT OVERS", 0)

    # ==========================
    # MATCH TITLE BANNER (HIGH CONTRAST)
    # ==========================

    st.markdown(f"""
    <div class="match-banner">
        <h2>📍 Focus Team vs {team1} @ {venue_label}</h2>
    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # KPI METRICS
    # ==========================

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("🎯 Total Matches", int(matches))

    with m2:
        st.metric("✅ Wins", int(win))

    with m3:
        st.metric("❌ Losses", int(lose))

    with m4:
        st.metric("📊 Win Rate", f"{winp:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================
    # INFORMATION CARDS (SCOPED HIGH CONTRAST)
    # ==========================

    left, right = st.columns(2)

    with left:
        st.markdown('<h3 class="page-title">🏏 Focus Team Performance</h3>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <h4>Focus Team Record</h4>
            <p>🔥 Highest Total : <b>{high}</b></p>
            <p>📉 Lowest Total : <b>{low}</b></p>
            <p>📊 Average Total : <b>{avg:.1f}</b></p>
            <p>⏱ Average Overs : <b>{avgovers}</b></p>
            <p>🎯 Average Wickets Lost : <b>{avgwkts}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f'<h3 class="page-title">⚔️ Opponent: {team1}</h3>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <h4>{team1} Record</h4>
            <p>🔥 Highest Total : <b>{high1}</b></p>
            <p>📉 Lowest Total : <b>{low1}</b></p>
            <p>📊 Average Total : <b>{avg1:.1f}</b></p>
            <p>⏱ Average Overs : <b>{avg3}</b></p>
            <p>🎯 Average Wickets Taken : <b>{avg2}</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # PERFORMANCE OVERVIEW CHARTS (PALETTE 1)
    # =====================================

    st.markdown("""
    <h2 class="page-title" style="margin-top:15px;">
    📊 Tactical Performance Breakdown
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # =====================================
    # DONUT CHART (PALETTE 1 OBSIDIAN & CYAN)
    # =====================================

    with col1:
        st.markdown('<h3 class="page-title">Win Distribution</h3>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(4.5, 4.2))
        fig.patch.set_facecolor("#111827")
        ax.set_facecolor("#111827")

        total_valid = win + lose
        chart_values = [win, lose] if total_valid > 0 else [1, 0]
        chart_colors = ["#0284C7", "#EF4444"] if total_valid > 0 else ["#334155", "#1E293B"]

        wedges, _ = ax.pie(
            chart_values,
            colors=chart_colors,
            startangle=90,
            wedgeprops=dict(
                width=0.35,
                edgecolor="#111827",
                linewidth=2
            )
        )

        ax.text(
            0,
            0,
            f"{winp:.1f}%\nWin Rate",
            ha="center",
            va="center",
            fontsize=15,
            color="#FFFFFF",
            fontweight="bold"
        )

        ax.legend(
            wedges,
            [f"Wins ({int(win)})", f"Losses ({int(lose)})"],
            loc="lower center",
            bbox_to_anchor=(0.5, -0.16),
            ncol=2,
            frameon=False,
            fontsize=10,
            labelcolor="#CBD5E1"
        )

        ax.axis("equal")
        st.pyplot(fig)
        plt.close(fig)

    # =====================================
    # BAR CHART (PALETTE 1 OBSIDIAN & CYAN)
    # =====================================

    with col2:
        st.markdown('<h3 class="page-title">Average Score Comparison</h3>', unsafe_allow_html=True)

        fig2, ax2 = plt.subplots(figsize=(5.2, 4.2))
        fig2.patch.set_facecolor("#111827")
        ax2.set_facecolor("#111827")

        bar_teams = ["Focus Team", team1]
        bar_scores = [avg, avg1]

        bars = ax2.bar(
            bar_teams,
            bar_scores,
            color=["#0284C7", "#38BDF8"],
            width=0.48,
            edgecolor="#1E293B",
            linewidth=1.5
        )

        ax2.tick_params(colors="#CBD5E1", labelsize=10)
        ax2.spines["bottom"].set_color("#334155")
        ax2.spines["left"].set_color("#334155")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.set_ylabel("Runs", color="#CBD5E1", fontsize=10)

        for bar in bars:
            h = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                h + 2.5,
                f"{h:.1f}",
                ha="center",
                fontsize=11,
                color="#FFFFFF",
                fontweight="bold"
            )

        st.pyplot(fig2)
        plt.close(fig2)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # PERFORMANCE STRENGTH METRICS
    # =====================================

    st.markdown("""
    <h2 class="page-title">
    📈 Relative Strength Indices
    </h2>
    """, unsafe_allow_html=True)

    c_s1, c_s2 = st.columns(2)

    with c_s1:
        st.markdown("**Focus Team Scoring Index (Par: 200)**")
        st.progress(min(avg / 250, 1.0))
        st.caption(f"Average: {avg:.1f} runs")

    with c_s2:
        st.markdown(f"**{team1} Scoring Index (Par: 200)**")
        st.progress(min(avg1 / 250, 1.0))
        st.caption(f"Average: {avg1:.1f} runs")

    st.markdown("**Head-to-Head Win Probability**")
    st.progress(min(winp / 100, 1.0))
    st.caption(f"Calculated Win Probability: {winp:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # MATCH INSIGHTS (DYNAMIC BENCHMARK)
    # =====================================

    st.markdown("""
    <h2 class="page-title">
    🧠 Tactical Match Intelligence
    </h2>
    """, unsafe_allow_html=True)

    if winp >= 70:
        st.success(
            f"🔥 **Dominant Track Record:** The focus team maintains a dominant {winp:.1f}% win rate against {team1} at {venue_label}. Historical matchups show a distinct tactical ceiling advantage."
        )
    elif winp >= 50:
        st.success(
            f"⚖️ **Even Contest:** Historical records indicate a competitive matchup with a slight tactical edge ({winp:.1f}% win rate) against {team1}."
        )
    else:
        st.error(
            f"⚠️ **Challenging Encounter:** Historical data indicates a demanding matchup ({winp:.1f}% win rate) against {team1}. Targeted phase planning and disciplined bowling will be key."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # STRATEGIC RECOMMENDATION (HIGH CONTRAST)
    # =====================================

    st.markdown(f"""
    <div class="info-card">
        <h3>🎯 Strategic Recommendation</h3>
        <p>
            Based on historical encounters against <b>{team1}</b> across <b>{matches}</b> matches, 
            the current win rate stands at <b>{winp:.1f}%</b>.
        </p>
        <p>
            When competing at <b>{venue_label}</b>, tactical bowling economies and powerplay phase containment 
            remain critical parameters to defend or surpass the historical average total of <b>{avg1:.1f}</b> runs.
        </p>
    </div>
    """, unsafe_allow_html=True)