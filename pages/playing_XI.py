import streamlit as st
import pandas as pd
import html
import base64
import os
from PIL import Image

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Playing XI | CricVision",
    layout="wide"
)

# =====================================================
# HIDE STREAMLIT UI & PALETTE 1 CSS
# =====================================================

st.markdown("""
<style>
header[data-testid="stHeader"] {
    background: transparent !important;
}

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

/* =====================================================
   PALETTE 1: OBSIDIAN GLASS & ALABASTER CANVAS THEME
===================================================== */

/* Canvas Background */
.stApp {
    background-color: #E5E4E0 !important;
    color: #0F172A;
}

.main .block-container {
    background: transparent;
    color: #0F172A;
}

h1, h2, h3, h4, h5, h6 {
    color: #0F172A !important;
    font-weight: 800;
}

p, span, label {
    color: #1E293B;
}

/* =========================
   SELECTBOX / SEARCH BAR FIX
========================= */

/* Label above dropdown */
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] label p {
    color: #0F172A !important;
    font-weight: 800 !important;
    font-size: 15px !important;
}

/* BaseWeb container */
div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1.5px solid #0284C7 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
}

/* Text and placeholder inside dropdown */
div[data-baseweb="select"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Dropdown arrow icon */
div[data-baseweb="select"] svg {
    fill: #0284C7 !important;
}

/* Dropdown menu list items */
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
   STATUS ALERTS & BANNERS FIX
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

/* =========================
   PLAYER CARDS (PALETTE 1)
========================= */

.player-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 16px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
    transition: 0.3s;
}

.player-card:hover {
    transform: translateY(-4px);
    border-color: #0284C7;
    box-shadow: 0 14px 30px rgba(2, 132, 199, 0.30);
}

.player-name {
    color: #FFFFFF !important;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 6px;
}

.player-role {
    color: #38BDF8 !important;
    font-size: 14px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 10px;
}

.player-stats {
    color: #CBD5E1 !important;
    font-size: 14px;
    line-height: 1.8;
}

.tag-captain {
    display: inline-block;
    background: #FBBF24;
    color: #111827 !important;
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
    margin-bottom: 6px;
}

.tag-vc {
    display: inline-block;
    background: #0284C7;
    color: #FFFFFF !important;
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
    margin-bottom: 6px;
}

/* =========================
   RECOMMENDATION CARDS
========================= */

.reco-card {
    background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
    padding: 20px;
    border-radius: 18px;
    border-left: 5px solid #0284C7;
    border-top: 1px solid #334155;
    border-right: 1px solid #334155;
    border-bottom: 1px solid #334155;
    margin-bottom: 14px;
    color: #F8FAFC !important;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
}

.reco-card b {
    color: #38BDF8;
}

hr {
    border-color: #CBD5E1 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD WIDE FULL BANNER LOGO
# =====================================================

def get_base64_banner():
    candidate_paths = [
        "logo.png",
        "Picsart_26-10-31_19-37-06-915.png",
        "banner.png",
        "cricvision_banner.png",
        "[logo].png"
    ]
    
    # Check both current directory and parent directory (for pages/ folder execution)
    all_paths = []
    for p in candidate_paths:
        all_paths.append(p)
        all_paths.append(os.path.join("..", p))
    
    # 1. First priority: find a wide banner image (width > height)
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

    # 2. Second priority: any available candidate image
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
    🏏 Playing XI Recommendation System
    </h1>
    <p style="font-size:16px; color:#475569; margin:0;">
    Generate the optimal match-day playing combination based on venue dynamics
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
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

    df = pd.read_excel(excel_path, sheet_name="PLAYING_XII_RECOMMENDATION")
    df1 = pd.read_excel(excel_path, sheet_name="NEW_PLAYER_DATA")

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()
    df1.columns = df1.columns.astype(str).str.strip()

    # Clean text columns
    for data in [df, df1]:
        for col in data.select_dtypes(include="object").columns:
            data[col] = data[col].apply(
                lambda value: value.strip() if isinstance(value, str) else value
            )

    return df, df1


try:
    df, df1 = load_data()
except Exception as e:
    st.error(f"Unable to load Excel data: {e}")
    st.stop()


# =====================================================
# REQUIRED COLUMN VALIDATION
# =====================================================

required_columns = [
    "Player_Name",
    "Role",
    "NATIONALITY",
    "Venue",
    "Performance_Score",
    "Strike_Rate",
    "Economy",
    "Batting_Rank",
    "Bowling_Rank",
    "All_Rounder_Rank",
    "Wk_Rank"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing columns in PLAYING_XII_RECOMMENDATION: {missing_columns}")
    st.stop()


# =====================================================
# ROLE NORMALIZATION
# =====================================================

def normalize_role(role):
    if pd.isna(role):
        return ""
    role = str(role).strip().lower()
    role_mapping = {
        "batsman": "Batsman",
        "wk-batsman": "WK-Batsman",
        "wicketkeeper": "WK-Batsman",
        "wicket keeper": "WK-Batsman",
        "bowler": "Bowler",
        "all rounder": "All Rounder",
        "all-rounder": "All Rounder",
        "allrounder": "All Rounder"
    }
    return role_mapping.get(role, str(role).strip())


df["Role"] = df["Role"].apply(normalize_role)

if "Role" in df1.columns:
    df1["Role"] = df1["Role"].apply(normalize_role)


# =====================================================
# NUMERIC CONVERSION
# =====================================================

numeric_columns = [
    "Performance_Score",
    "Strike_Rate",
    "Economy",
    "Batting_Rank",
    "Bowling_Rank",
    "All_Rounder_Rank",
    "Wk_Rank"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in [
    "Performance_Score",
    "Strike_Rate",
    "Economy",
    "Batting_score",
    "All_Rounder_score"
]:
    if col in df1.columns:
        df1[col] = pd.to_numeric(df1[col], errors="coerce")


# =====================================================
# SELECT VENUE
# =====================================================

unique_venues = sorted(df["Venue"].dropna().unique().tolist())

if not unique_venues:
    st.error("No venues found in the Excel dataset.")
    st.stop()

venue = st.selectbox(
    "Select Venue",
    unique_venues,
    index=None,
    placeholder="Choose Venue"
)

generate = st.button("🚀 Generate Playing XI")


if venue is None or not generate:
    st.stop()


# =====================================================
# MAIN LOGIC
# =====================================================

st.markdown(f"### 📍 Selected Venue: {venue}")

filtered = df[
    df["Venue"].astype(str).str.strip() == str(venue).strip()
].copy()


if filtered.empty:
    st.warning("No player records found for this venue.")
    st.stop()


# =====================================================
# ROLE-BASED PLAYER SELECTION
# =====================================================

def select_category(role, rank_column, count):
    category = filtered[filtered["Role"] == role].copy()
    if category.empty:
        return category

    ranked = category.dropna(subset=[rank_column]).sort_values(by=rank_column, ascending=True)
    selected = ranked.head(count)

    if len(selected) < count:
        remaining = category[~category.index.isin(selected.index)].copy()
        remaining = remaining.dropna(subset=["Performance_Score"]).sort_values(by="Performance_Score", ascending=False)
        needed = count - len(selected)
        selected = pd.concat([selected, remaining.head(needed)])

    return selected.head(count)


bat = select_category("Batsman", "Batting_Rank", 2)
wk = select_category("WK-Batsman", "Wk_Rank", 1)
all_rounders = select_category("All Rounder", "All_Rounder_Rank", 4)
bowl = select_category("Bowler", "Bowling_Rank", 4)


# =====================================================
# COMBINE SQUAD
# =====================================================

squad = pd.concat([bat, wk, all_rounders, bowl], ignore_index=True)
squad = squad.reindex(columns=filtered.columns)

if "Role" not in squad.columns:
    squad["Role"] = pd.Series(dtype="object")


# =====================================================
# OVERSEAS PLAYER LIMIT
# =====================================================

if not squad.empty:
    indian_players = squad[
        squad["NATIONALITY"].astype(str).str.strip().str.lower() == "indian"
    ]
    overseas_players = squad[
        squad["NATIONALITY"].astype(str).str.strip().str.lower() == "overseas"
    ]
    squad = pd.concat([indian_players, overseas_players.head(4)], ignore_index=True)


if squad.empty:
    st.error("No players could be selected. Please check role and performance data.")
    st.stop()


# =====================================================
# PLAYING XI DISPLAY (ZERO-INDENTED HTML RENDERING)
# =====================================================

st.divider()

st.markdown("### 🧾 Final Playing XI")

st.info(f"Players selected: {len(squad)} / 11")

if len(squad) < 11:
    st.warning("Fewer than 11 players were selected. Check venue records.")

cols = st.columns(2)

for i, (_, row) in enumerate(squad.iterrows()):
    tag_html = ""

    # Captain (Constant)
    if row["Player_Name"] == "Shubman Gill":
        tag_html = '<span class="tag-captain">👑 Captain</span>'

    # Vice Captain (Constant)
    elif row["Player_Name"] == "Rashid Khan":
        tag_html = '<span class="tag-vc">⭐ Vice Captain</span>'

    sr = pd.to_numeric(row["Strike_Rate"], errors="coerce")
    eco = pd.to_numeric(row["Economy"], errors="coerce")

    sr_text = f"{sr:.2f}" if pd.notna(sr) else "N/A"
    eco_text = f"{eco:.2f}" if pd.notna(eco) else "N/A"

    player_name = html.escape(str(row["Player_Name"]))
    player_role = html.escape(str(row["Role"]))

    # Clean single-line HTML string: Markdown will NOT parse this as a code block!
    card_html = (
        f'<div class="player-card">'
        f'<div class="player-name">👤 {player_name}</div>'
        f'{tag_html}'
        f'<div class="player-role">🎯 {player_role}</div>'
        f'<div class="player-stats">'
        f'⚡ Strike Rate: {sr_text}<br>'
        f'🔴 Economy: {eco_text}'
        f'</div>'
        f'</div>'
    )

    with cols[i % 2]:
        st.markdown(card_html, unsafe_allow_html=True)


# =====================================================
# SUGGESTED IMPROVEMENTS
# =====================================================

st.divider()
st.markdown("### 🔁 Suggested Improvements")
found = False


def show_recommendation(old_name, new_name, reason):
    old_name = html.escape(str(old_name))
    new_name = html.escape(str(new_name))
    reason = html.escape(str(reason))
    reco_html = (
        f'<div class="reco-card">'
        f'⭐ Replace <b>{old_name}</b> with <b>{new_name}</b><br>'
        f'{reason}'
        f'</div>'
    )
    st.markdown(reco_html, unsafe_allow_html=True)


# =====================================================
# BOWLER RECOMMENDATIONS
# =====================================================

bowlers = squad[squad["Role"] == "Bowler"]
eco_low = bowlers[bowlers["Economy"] >= 10]

if "Role" in df1.columns and "Economy" in df1.columns:
    new_bowlers = df1[df1["Role"] == "Bowler"].sort_values(by="Economy", ascending=True).head(1)
    for j in range(min(len(eco_low), len(new_bowlers))):
        old = eco_low.iloc[j]
        new = new_bowlers.iloc[j]
        found = True
        show_recommendation(
            old["Player_Name"],
            new["Player_Name"],
            f"Better economy ({old['Economy']:.2f} → {new['Economy']:.2f})"
        )


# =====================================================
# BATSMAN RECOMMENDATIONS
# =====================================================

batters = squad[squad["Role"] == "Batsman"]
all_low = batters[batters["Performance_Score"] >= 60]

if "Role" in df1.columns and "Batting_score" in df1.columns:
    new_all = df1[df1["Role"] == "Batsman"].sort_values(by="Batting_score", ascending=True).head(1)
    for j in range(min(len(all_low), len(new_all))):
        old = all_low.iloc[j]
        new = new_all.iloc[j]
        found = True
        show_recommendation(
            old["Player_Name"],
            new["Player_Name"],
            "Better batting performance score."
        )


# =====================================================
# ALL-ROUNDER RECOMMENDATIONS
# =====================================================

allrounders = squad[squad["Role"] == "All Rounder"]
all_low1 = allrounders[allrounders["Performance_Score"] >= 20]

if "Role" in df1.columns and "All_Rounder_score" in df1.columns:
    new_all1 = df1[df1["Role"] == "All Rounder"].sort_values(by="All_Rounder_score", ascending=True).head(1)
    for j in range(min(len(all_low1), len(new_all1))):
        old = all_low1.iloc[j]
        new = new_all1.iloc[j]
        found = True
        show_recommendation(
            old["Player_Name"],
            new["Player_Name"],
            "Better all-round performance."
        )


# =====================================================
# WICKETKEEPER RECOMMENDATIONS
# =====================================================

wk1 = squad[squad["Role"] == "WK-Batsman"]
all_low2 = wk1[wk1["Performance_Score"] >= 30]

if "Role" in df1.columns and "Batting_score" in df1.columns:
    new_all2 = df1[df1["Role"] == "WK-Batsman"].sort_values(by="Batting_score", ascending=True).head(1)
    for j in range(min(len(all_low2), len(new_all2))):
        old = all_low2.iloc[j]
        new = new_all2.iloc[j]
        found = True
        show_recommendation(
            old["Player_Name"],
            new["Player_Name"],
            "Better wicketkeeper batting performance."
        )


# =====================================================
# FINAL MESSAGE
# =====================================================

if not found:
    st.info("No major improvements suggested. Current Playing XI looks balanced.")