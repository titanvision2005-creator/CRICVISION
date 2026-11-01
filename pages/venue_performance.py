import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
from PIL import Image

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Venue Intelligence | CricVision",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# PALETTE 1 CSS (OBSIDIAN GLASS & ALABASTER CANVAS)
# ==========================================

st.markdown("""
<style>
/* Hide Streamlit Chrome */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1200px;
}

[data-testid="stToolbar"] {
    display: none;
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
    color: #0F172A;
}

/* Page Outer Section Titles */
h1.page-title, h2.page-title, h3.page-title {
    color: #0F172A !important;
    font-weight: 900 !important;
    margin-top: 25px;
    margin-bottom: 15px;
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

ul[role="listbox"] {
    background-color: #111827 !important;
    border: 1px solid #0284C7 !important;
}

ul[role="listbox"] li {
    color: #F8FAFC !important;
    background-color: #111827 !important;
}

ul[role="listbox"] li:hover {
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
   KPI METRIC CARDS
========================= */

.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #0284C7;
    box-shadow: 0 14px 30px rgba(2, 132, 199, 0.30);
}

.metric-value {
    font-size: 34px;
    font-weight: 900;
    color: #38BDF8;
}

.metric-label {
    font-size: 14px;
    font-weight: 700;
    color: #CBD5E1;
    margin-top: 4px;
}

/* =========================
   INFO & STADIUM CARDS
========================= */

.info-card, .stadium-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #334155;
    border-left: 5px solid #0284C7;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    color: #E2E8F0;
    margin-bottom: 16px;
    line-height: 1.8;
}

.info-card h4, .stadium-card h4 {
    color: #38BDF8 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin-top: 0 !important;
    margin-bottom: 12px !important;
}

.info-card b, .stadium-card b {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Tags */
.tag {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 800;
}

.good {
    background: #0284C7;
    color: #FFFFFF;
}

.bad {
    background: #BE123C;
    color: #FFE4E6;
}

/* Alerts */
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

.stProgress > div > div > div > div {
    background-color: #0284C7 !important;
}

.stCaption, [data-testid="stCaptionContainer"] p {
    color: #334155 !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD WIDE BANNER LOGO
# ==========================================

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

# ==========================================
# HEADER
# ==========================================

if banner_logo:
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 15px 0;">
        <img src="data:image/png;base64,{banner_logo}" style="width:100%; max-width:620px; height:auto; border-radius:12px;">
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom: 25px;">
    <h1 style="font-size:38px; font-weight:900; color:#0F172A; margin:0 0 6px 0;">
    🏟 Venue Intelligence Center
    </h1>
    <p style="font-size:16px; color:#475569; margin:0;">
    Transforming Venue Data & Match Splits into Winning Decisions
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA (DYNAMIC FILE RESOLUTION)
# ==========================================

@st.cache_data
def load_venue_data():
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

    df_v = pd.read_excel(excel_path, sheet_name="VENUE_PERFORMANCE")
    df_v.columns = df_v.columns.astype(str).str.strip()
    return df_v

try:
    df = load_venue_data()
except Exception as e:
    st.error(f"Unable to load Venue dataset: {e}")
    st.stop()

# ==========================================
# VENUE SELECTOR & BUTTON
# ==========================================

venues = sorted(df["Venue"].dropna().unique().tolist())

venue = st.selectbox(
    "Select Venue",
    venues,
    index=None,
    placeholder="Choose Venue"
)

analyze = st.button("🚀 View Venue Analysis")

if not analyze:
    st.stop()

if venue is None:
    st.warning("Please select a venue to generate the analysis.")
    st.stop()

filtered = df[df["Venue"].astype(str).str.strip() == str(venue).strip()]

if filtered.empty:
    st.warning("No data available for this venue.")
    st.stop()

row = filtered.iloc[0]

matches = int(row.get("Matches played", 0))
wins = int(row.get("Wins", 0))
losses = int(row.get("Losses", 0))
win_percent = round(float(row.get("Win%", 0)), 1)

# ==========================================
# VENUE HEADER
# ==========================================

st.markdown(f'<h2 class="page-title">📍 {venue}</h2>', unsafe_allow_html=True)

if win_percent >= 60:
    st.markdown("<span class='tag good'>🔥 High Win Rate Venue</span>", unsafe_allow_html=True)
else:
    st.markdown("<span class='tag bad'>⚠️ Highly Competitive Venue</span>", unsafe_allow_html=True)

st.write("")

# ==========================================
# KPI CARDS (PALETTE 1 OBSIDIAN)
# ==========================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{matches}</div>
            <div class="metric-label">🏏 Matches</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{wins}</div>
            <div class="metric-label">✅ Wins</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{losses}</div>
            <div class="metric-label">❌ Losses</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{win_percent}%</div>
            <div class="metric-label">📊 Win Rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ==========================================
# VENUE STRENGTH
# ==========================================

st.markdown('<h3 class="page-title">🎯 Venue Index Rating</h3>', unsafe_allow_html=True)

rating = min(round(win_percent / 10, 1), 10.0)
st.progress(rating / 10)
st.caption(f"Venue Rating Index: {rating:.1f} / 10.0")

st.write("")

# ==========================================
# MAIN LAYOUT (PALETTE 1 HIGH CONTRAST)
# ==========================================

left, right = st.columns([1.1, 1])

with left:
    st.markdown(f"""
    <div class="stadium-card">
        <h4>🏟 Venue Overview</h4>
        Historical team performance benchmark at <b>{venue}</b> across all recorded competitive fixtures.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
        <h4>🧠 Tactical Summary</h4>
        The squad has contested <b>{matches}</b> fixtures at <b>{venue}</b>, securing 
        <b>{wins}</b> victories with a calculated win efficiency of <b>{win_percent}%</b>.
        <br><br>
        Match dynamics at this venue highlight critical tactical inflection points during powerplay containment 
        and backend boundary execution.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if win_percent >= 75:
        st.success("🏆 Exceptional track record with consistently dominant performances at this venue.")
    elif win_percent >= 60:
        st.success("💪 Strong venue with a proven historical advantage.")
    elif win_percent >= 45:
        st.warning("⚖️ Balanced venue with competitive, evenly contested results.")
    elif win_percent >= 30:
        st.warning("📉 Below average win conversion record at this venue.")
    else:
        st.error("🚫 Historically demanding venue requiring strategic squad adjustments.")

with right:
    st.markdown('<h3 class="page-title" style="margin-top:0;">📊 Performance Split</h3>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    total_matches = wins + losses
    chart_vals = [wins, losses] if total_matches > 0 else [1, 0]
    chart_colors = ["#0284C7", "#EF4444"] if total_matches > 0 else ["#334155", "#1E293B"]

    wedges, _ = ax.pie(
        chart_vals,
        labels=None,
        colors=chart_colors,
        startangle=90,
        wedgeprops=dict(width=0.35, edgecolor="#111827", linewidth=2)
    )

    ax.text(
        0,
        0,
        f"{win_percent}%",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="#FFFFFF"
    )

    ax.axis("equal")
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 10px;">
            <span style="color:#38BDF8; font-weight:800; font-size:15px;">
                ● Wins ({wins})
            </span>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <span style="color:#EF4444; font-weight:800; font-size:15px;">
                ● Losses ({losses})
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )