import streamlit as st
import base64
import os

st.set_page_config(
    page_title="CricVision",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# HIDE STREAMLIT UI
# =========================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B0F19, #111827);
    border-right: 2px solid #0284C7;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD LOGO (DYNAMIC LOOKUP)
# =========================
def get_base64_logo():
    possible_names = [
        "Picsart_26-10-31_19-37-06-915.png",
        "input_file_2.png",
        "[logo].png",
        "logo.png",
        "logo.jpg"
    ]
    for path in possible_names:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                continue
    return ""

logo = get_base64_logo()


# =========================
# PALETTE 1: OBSIDIAN GLASS & ALABASTER CANVAS CSS
# =========================
st.markdown("""
<style>

/* APP BACKGROUND: LOGO OYSTER CHALK */
.stApp {
    background-color: #E5E4E0 !important;
    color: #0F172A;
}

/* HERO CONTAINER */
.hero {
    text-align: center;
    padding: 20px 20px 10px 20px;
}

.hero img {
    max-width: 320px;
    height: auto;
    border-radius: 12px;
}

/* SECTION TITLES */
.section-title {
    margin-top: 35px;
    font-size: 26px;
    font-weight: 900;
    color: #0F172A;
    border-bottom: 3px solid #0284C7;
    padding-bottom: 8px;
    margin-bottom: 22px;
    letter-spacing: 0.5px;
}

/* STAT CARDS: OBSIDIAN SLATE */
.stat-card {
    background: #111827;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    border: 1px solid #1E293B;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
    transition: 0.3s;
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: #0284C7;
    box-shadow: 0 12px 28px rgba(2, 132, 199, 0.20);
}

.stat-number {
    font-size: 34px;
    font-weight: 900;
    color: #0284C7;
}

.stat-label {
    color: #CBD5E1;
    font-size: 15px;
    font-weight: 600;
    margin-top: 2px;
}

/* FEATURE CARD: MIDNIGHT SLATE GRADIENT */
.feature-card {
    background: linear-gradient(135deg, #1E293B, #0F172A);
    border-radius: 22px;
    padding: 28px;
    height: 180px;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14);
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 16px 36px rgba(2, 132, 199, 0.28);
    border-color: #0284C7;
}

.icon {
    font-size: 42px;
}

.feature-title {
    color: #F8FAFC;
    font-size: 21px;
    font-weight: 800;
    margin-top: 6px;
}

.feature-desc {
    color: #94A3B8;
    margin-top: 6px;
    font-size: 14px;
    line-height: 1.4;
}

/* PLAYING XI SPECIAL CARD */
.xi-card {
    background: linear-gradient(135deg, #0B0F19 0%, #1E293B 100%);
    border-radius: 26px;
    padding: 42px 30px;
    text-align: center;
    border: 2px solid #0284C7;
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.22);
    margin-bottom: 15px;
}

.xi-title {
    font-size: 40px;
    font-weight: 900;
    color: #F8FAFC;
    letter-spacing: 0.5px;
}

.xi-text {
    font-size: 17px;
    color: #CBD5E1;
    max-width: 750px;
    margin: 12px auto 0 auto;
    line-height: 1.6;
}

/* ACTION BUTTONS */
.stButton button {
    width: 100%;
    height: 46px;
    border-radius: 14px;
    background: #0284C7;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 15px;
    border: none;
    margin-top: 10px;
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.30);
    transition: 0.3s;
}

.stButton button:hover {
    background: #0369A1;
    color: #FFFFFF;
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(2, 132, 199, 0.45);
}

</style>
""", unsafe_allow_html=True)


# =========================
# HERO (SEAMLESS LOGO INTEGRATION)
# =========================
if logo:
    st.markdown(f"""
    <div class="hero">
        <img src="data:image/png;base64,{logo}" alt="CricVision">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero">
        <h1 style="font-size:56px; font-weight:900; color:#0F172A; margin:0;">CricVision</h1>
        <p style="font-size:18px; color:#475569; margin-top:5px;">Cricket, Decoded 🏏</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# EXACT STAT BOXES (OBSIDIAN ON ALABASTER)
# =========================
c1, c2, c3, c4 = st.columns(4)

stats = [
    ("13", "Venues"),
    ("700+", "Players"),
    ("10", "Squads"),
    ("1192", "Matches")
]

for col, data in zip([c1, c2, c3, c4], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{data[0]}</div>
            <div class="stat-label">{data[1]}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# TEAM PERFORMANCE ANALYSIS (3 MODULES)
# =========================
st.markdown("""
<div class="section-title">
🏟 TEAM PERFORMANCE ANALYSIS
</div>
""", unsafe_allow_html=True)

a, b, c = st.columns(3)

cards = [
    ("🏟", "Venue Analysis", "Venue trends & match winning decisions", "pages/venue_performance.py"),
    ("⚔️", "Opponent Analysis", "Opposition study & head-to-head records", "pages/opponent.py"),
    ("🎯", "Venue Specialists", "Best performers & venue impact metrics", "pages/venue_player_performance.py")
]

for col, item in zip([a, b, c], cards):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">{item[0]}</div>
            <div class="feature-title">{item[1]}</div>
            <div class="feature-desc">{item[2]}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open", key=item[1]):
            st.switch_page(item[3])


# =========================
# SQUAD EXPLORER (SEPARATE)
# =========================
st.markdown("""
<div class="section-title">
👥 SQUAD EXPLORER
</div>
""", unsafe_allow_html=True)

sq_left, sq_mid, sq_right = st.columns([1, 2, 1])

with sq_mid:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">👥</div>
        <div class="feature-title">Squad Explorer</div>
        <div class="feature-desc">Explore squads, player profiles, and combinations</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Squad Explorer", key="btn_squad_standalone"):
        st.switch_page("pages/squad.py")


# =========================
# PLAYING XI (MAIN FLAGSHIP MODULE - SEPARATE)
# =========================
st.markdown("""
<div class="section-title">
🏏 PLAYING XI RECOMMENDATION SYSTEM
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="xi-card">
    <div class="xi-title">Generate Best Playing XI</div>
    <div class="xi-text">
        Create venue-based and opponent-specific playing combinations using multi-parameter cricket intelligence, overseas constraints, and role-balanced optimization.
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Launch Playing XI Builder", key="btn_launch_xi"):
    st.switch_page("pages/playing_XI.py")