import streamlit as st
import pandas as pd
import base64
import os
from PIL import Image

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Venue Specialists | CricVision",
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
   MAIN CARD (HIGH CONTRAST OBSIDIAN)
========================= */

.card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #334155;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    transition: 0.3s;
    margin-bottom: 14px;
}

.card:hover {
    transform: translateY(-4px);
    border-color: #0284C7;
    box-shadow: 0 14px 30px rgba(2, 132, 199, 0.28);
}

.card h2 {
    color: #FFFFFF !important;
    margin: 0 !important;
    font-size: 24px !important;
    font-weight: 900 !important;
}

.card h3 {
    font-size: 19px !important;
    font-weight: 800 !important;
    margin-top: 0 !important;
    margin-bottom: 14px !important;
}

.card p {
    color: #E2E8F0 !important;
    font-size: 14.5px !important;
    line-height: 1.8 !important;
    margin-bottom: 6px !important;
}

.card b {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Tags */
.tag {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 800;
}

.tag.avg {
    background: #0284C7;
    color: #FFFFFF !important;
}

/* Status Alerts */
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

hr {
    border: none;
    border-top: 1.5px solid #CBD5E1;
    margin: 20px 0;
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
    🎯 Venue Player Intelligence
    </h1>
    <p style="font-size:16px; color:#475569; margin:0;">
    Analyze Venue-Specific Player Performance, Quotas & Match Impact
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA (DYNAMIC FILE RESOLUTION)
# ==========================================

@st.cache_data
def load_venue_player_data():
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

    df_vp = pd.read_excel(excel_path, sheet_name="VENUE_WISE_PLAYER_PERFORMANCE")
    df_vp.columns = df_vp.columns.astype(str).str.strip()
    return df_vp

try:
    df = load_venue_player_data()
except Exception as e:
    st.error(f"Unable to load Venue Player dataset: {e}")
    st.stop()

# ==========================================
# FILTERS
# ==========================================

c1, c2 = st.columns(2)

with c1:
    unique_venues = sorted(df["Venue"].dropna().unique().tolist())
    venue = st.selectbox("Select Venue", unique_venues, index=None, placeholder="Choose Venue")

with c2:
    unique_players = sorted(df["Player_Name"].dropna().unique().tolist())
    player = st.selectbox("Select Player", unique_players, index=None, placeholder="Choose Player")

analyze = st.button("🚀 View Venue Specialist Analysis")

# ==========================================
# MAIN LOGIC
# ==========================================

if analyze and venue is not None and player is not None:

    filtered = df[(df["Venue"].astype(str).str.strip() == str(venue).strip()) & 
                  (df["Player_Name"].astype(str).str.strip() == str(player).strip())]

    if filtered.empty:
        st.warning(f"No match records found for {player} at {venue}.")
    else:
        rows = filtered.iloc[0]

        Name = rows.get('Player_Name', player)
        Role = rows.get('Role', 'Specialist')
        Matches = rows.get('Matches_played', 0)

        runs = rows.get('Runs', 0)
        balls = rows.get('Balls', 0)
        runs_conceded = rows.get('Runs_Conceded', 0)
        wickets = rows.get('Wickets', 0)
        Overs = rows.get('Overs', 0)
        Economy = float(pd.to_numeric(rows.get('Economy', 0), errors='coerce') or 0)
        sr = float(pd.to_numeric(rows.get('Strike rate', 0), errors='coerce') or 0)
        avg = float(pd.to_numeric(rows.get('Average', 0), errors='coerce') or 0)

        # =========================
        # HEADER CARD
        # =========================
        st.markdown(f"""
        <div class="card" style="border-left: 5px solid #0284C7;">
            <h2>👤 {Name}</h2>
            <p style="margin-top: 8px;">
                <span class="tag avg">{Role}</span>
                &nbsp;&nbsp; 
                <span style="color:#CBD5E1; font-weight:700;">🏟️ {venue}</span>
            </p>
            <p style="color:#38BDF8; font-weight:700; margin:0;">
                📊 Matches Contested: {Matches}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # PERFORMANCE TAGS
        # =========================
        col_tag1, col_tag2 = st.columns(2)

        with col_tag1:
            if sr >= 140:
                st.success("🔥 High strike-rate venue impact")
            elif sr > 0 and sr < 100:
                st.warning("⚠️ Restricted scoring rate at this venue")
            elif sr == 0:
                st.info("No Batting Quota Contested")
            else:
                st.info("⚖️ Stable batting baseline at this venue")

        with col_tag2:
            if Economy > 0 and Economy < 7:
                st.success("🎯 Highly economical venue containment")
            elif Economy >= 9.5:
                st.error("⚠️ Elevated venue economy conceded")
            elif Economy == 0:
                st.info("No Bowling Record Found")
            else:
                st.info("⚖️ Balanced bowling phase control")

        st.markdown("<hr>", unsafe_allow_html=True)

        # =========================
        # 2 COLUMN LAYOUT (BATTING | BOWLING)
        # =========================
        col1, col2 = st.columns(2)

        # =========================
        # BATTING CARD
        # =========================
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3 style="color:#38BDF8;">🏏 Batting Metrics</h3>
                <p>⚾ Balls Faced: <b>{balls}</b></p>
                <p>⚡ Total Runs: <b>{runs}</b></p>
                <p>🚀 Strike Rate: <b>{sr:.2f}</b></p>
                <p>📈 Batting Average: <b>{avg:.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Strike Rate Index**")
            st.progress(min(sr / 200, 1.0))
            st.caption(f"Strike Rate: {sr:.2f}")

            st.markdown("**Consistency Average**")
            st.progress(min(avg / 80, 1.0))
            st.caption(f"Average: {avg:.2f}")

            if runs >= 50:
                st.success("🏟️ High-ceiling batting venue for player")
            elif runs > 0:
                st.info("⚖️ Moderate batting return recorded here")
            else:
                st.warning("📉 Limited batting sample size at this venue")

        # =========================
        # BOWLING CARD
        # =========================
        with col2:
            st.markdown(f"""
            <div class="card">
                <h3 style="color:#38BDF8;">🔴 Bowling Metrics</h3>
                <p>⚾ Overs Bowled: <b>{Overs}</b></p>
                <p>💥 Runs Conceded: <b>{runs_conceded}</b></p>
                <p>📉 Economy Rate: <b>{Economy:.2f}</b></p>
                <p>🏏 Wickets Taken: <b>{wickets}</b></p>
            </div>
            """, unsafe_allow_html=True)

            if wickets > 0 or Economy > 0:
                st.markdown("**Economy Control Index**")
                st.progress(min(Economy / 12, 1.0))
                st.caption(f"Economy: {Economy:.2f}")

                if wickets >= 3:
                    st.success("🔥 High-impact wicket-taking strike record")
                else:
                    st.info("⚖️ Reliable phase containment bowling")
            else:
                st.info("Specialist batter / quota not deployed at this venue")

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # FINAL INSIGHT
        # =========================
        st.markdown('<h3 class="page-title">🧠 Match Intelligence Assessment</h3>', unsafe_allow_html=True)

        if "Batsman" in Role or "WK" in Role:
            if runs >= 50 or sr >= 140:
                st.success("Proven high-impact batting asset at this venue under tactical conditions.")
            else:
                st.info("Baseline batting contributor; match situation dependent.")
        elif "Bowler" in Role:
            if wickets >= 3 or (Economy < 7.5 and Economy > 0):
                st.success("Primary bowling asset with venue-proven economy and wicket frequency.")
            else:
                st.info("Standard containment bowler across venue middle overs.")
        else:
            if runs > runs_conceded:
                st.success("Effective dual-threat all-rounder offering distinct batting leverage.")
            else:
                st.info("Balanced venue contributor across bowling quotas and lower-order runs.")