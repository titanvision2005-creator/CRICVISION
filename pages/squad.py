import streamlit as st
import pandas as pd
import base64
import os
from PIL import Image

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Squad Explorer | CricVision",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# PALETTE 1 CSS (OBSIDIAN GLASS & ALABASTER CANVAS)
# =====================================================

st.markdown("""
<style>
/* Hide default chrome */
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
h1.page-title, h2.page-title {
    color: #0F172A !important;
    font-weight: 900 !important;
    border-bottom: 3px solid #0284C7;
    padding-bottom: 8px;
    margin-top: 35px;
    margin-bottom: 20px;
}

/* =========================
   SEARCH INPUT STYLING
========================= */

div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p {
    color: #0F172A !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

div[data-baseweb="input"] > div {
    background-color: #111827 !important;
    border: 1.5px solid #0284C7 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
}

div[data-baseweb="input"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-size: 15px !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

/* =========================
   VERTICAL SEPARATOR & CARDS
========================= */

.vertical-line {
    border-left: 2px solid #0284C7;
    height: 100%;
    margin: 0 auto;
    min-height: 160px;
}

.player-header-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 22px 24px;
    border-radius: 18px;
    border: 1.5px solid #0284C7;
    margin-bottom: 14px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    transition: 0.3s;
}

.player-header-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(2, 132, 199, 0.28);
}

.player-header-card h2 {
    color: #FFFFFF !important;
    margin: 0 0 6px 0 !important;
    font-size: 24px !important;
    font-weight: 900 !important;
}

.player-sub-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #334155;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
    margin-bottom: 12px;
}

.player-sub-card h4 {
    margin-top: 0 !important;
    margin-bottom: 10px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
}

.player-sub-card p {
    color: #E2E8F0 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    margin: 4px 0 !important;
}

.player-sub-card b {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Captions and progress bars */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #334155 !important;
    font-weight: 700 !important;
}

.stProgress > div > div > div > div {
    background-color: #0284C7 !important;
}

hr.player-divider {
    border: none;
    border-top: 1.5px solid #CBD5E1;
    margin: 25px 0 35px 0;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD WIDE BANNER LOGO
# =====================================================

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

# =====================================================
# HEADER (WIDE FULL BANNER)
# =====================================================

if banner_logo:
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 15px 0;">
        <img src="data:image/png;base64,{banner_logo}" style="width:100%; max-width:620px; height:auto; border-radius:12px;">
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom: 25px;">
    <h1 style="font-size:38px; font-weight:900; color:#0F172A; margin:0 0 6px 0;">
    👥 Squad Explorer
    </h1>
    <p style="font-size:16px; color:#475569; margin:0;">
    Comprehensive Squad Analytics, Tactical Roles & Performance Profiles
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA (DYNAMIC FILE RESOLUTION)
# =====================================================

@st.cache_data
def load_squad_data():
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

    df_squad = pd.read_excel(excel_path, sheet_name="MY_SQUAD")
    df_squad.columns = df_squad.columns.astype(str).str.strip()
    return df_squad

try:
    df = load_squad_data()
except Exception as e:
    st.error(f"Unable to load Squad Excel sheet: {e}")
    st.stop()

# =====================================================
# SEARCH FILTER
# =====================================================

search = st.text_input("🔍 Search Player by Name", placeholder="Type player name...")

if search:
    df = df[df["Player_Name"].astype(str).str.contains(search, case=False, na=False)]

if df.empty:
    st.warning("No players matched your search criteria.")
    st.stop()

# =====================================================
# ROLE GROUPING & PLAYER CARDS
# =====================================================

roles = ["Batsman", "WK-Batsman", "All Rounder", "Bowler"]

for role in roles:
    role_df = df[df["Role"].astype(str).str.strip() == role]

    if role_df.empty:
        continue

    st.markdown(f'<h2 class="page-title">{role}s</h2>', unsafe_allow_html=True)

    for index, rows in role_df.iterrows():
        player_name = str(rows.get("Player_Name", "Unknown"))
        player_role = str(rows.get("Role", role))
        nationality = str(rows.get("Nationality", "N/A"))
        matches_played = rows.get("Matches", 0)

        # Player Header Card (High Contrast Obsidian & Cyan)
        st.markdown(f"""
        <div class="player-header-card">
            <h2>👤 {player_name}</h2>
            <div style="margin-top: 8px;">
                <span style="background:#0284C7; color:#FFFFFF; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:800; display:inline-block;">
                    {player_role}
                </span>
                &nbsp;&nbsp;
                <span style="color:#CBD5E1; font-size:14px; font-weight:600;">
                    🌍 {nationality}
                </span>
                &nbsp;&nbsp;
                <span style="color:#38BDF8; font-size:14px; font-weight:700;">
                    📊 Matches: {matches_played}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, mid, col2 = st.columns([1, 0.05, 1])

        # Batting Column
        with col1:
            bat_style = rows.get("Batting Style", "N/A")
            runs = rows.get("Runs", 0)
            centuries_fifties = rows.get("50S/100S", "0/0")
            sr_val = float(pd.to_numeric(rows.get("Strike Rate", 0), errors="coerce") or 0)
            avg_val = float(pd.to_numeric(rows.get("Average", 0), errors="coerce") or 0)

            st.markdown(f"""
            <div class="player-sub-card">
                <h4 style="color:#38BDF8;">🏏 Batting Metrics</h4>
                <p>Batting Style: <b>{bat_style}</b></p>
                <p>Total Runs: <b>{runs}</b></p>
                <p>50s / 100s: <b>{centuries_fifties}</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Strike Rate**")
            st.progress(min(sr_val / 200, 1.0))
            st.caption(f"Strike Rate: {sr_val:.2f}")

            st.markdown("**Batting Average**")
            st.progress(min(avg_val / 80, 1.0))
            st.caption(f"Average: {avg_val:.2f}")

        # Vertical Divider
        with mid:
            st.markdown('<div class="vertical-line"></div>', unsafe_allow_html=True)

        # Bowling Column
        with col2:
            wickets = pd.to_numeric(rows.get("Wickets", 0), errors="coerce") or 0
            eco_val = float(pd.to_numeric(rows.get("Economy", 0), errors="coerce") or 0)
            four_five_w = rows.get("4WS/5WS", "0/0")

            if wickets == 0 and eco_val == 0:
                st.markdown("""
                <div class="player-sub-card">
                    <h4 style="color:#94A3B8;">🔴 Bowling Metrics</h4>
                    <p>Primarily a specialist batsman / minimal bowling quota recorded.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="player-sub-card">
                    <h4 style="color:#38BDF8;">🔴 Bowling Metrics</h4>
                    <p>Wickets Taken: <b>{wickets}</b></p>
                    <p>Economy Rate: <b>{eco_val:.2f}</b></p>
                    <p>4Ws / 5Ws: <b>{four_five_w}</b></p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Economy Control (Par: 8.0)**")
                st.progress(min(eco_val / 12, 1.0))
                st.caption(f"Economy: {eco_val:.2f}")

        st.markdown('<hr class="player-divider">', unsafe_allow_html=True)