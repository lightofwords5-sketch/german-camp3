import subprocess
import sys
try:
    from groq import Groq
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    from groq import Groq


# ═══════════════════════════════════════════════════════════════════
#  GERMAN MASTERY CAMP  —  Professional Edition
#  Full-Stack Streamlit App | Auth + Admin + AI + Games + Progress
# ═══════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import json
import random
import datetime
import time
import re
import gspread
import bcrypt


# module imports after refactor
from auth import hash_pw, check_pw, get_user, register_user, login_user, update_user_xp
from data_manager import load_sheet, write_row, update_cell_by_key, get_gsheet_client
from ai_engine import ai_chat as engine_chat, ai_grammar_fixer
from ui_components import *
from dictionary import *
from config import tr

# initialize AI client (Groq)
client = Groq(api_key=st.secrets.get('GROQ_API_KEY',''))

AI_AVAILABLE = True  # set to True if GROQ key exists

# ────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇩🇪 German Mastery Camp",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────────
#  CSS  — Black / Red / Gold palette
# ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

:root{
  --black:#0d0d0d; --red:#cc0000; --gold:#f5c518; --gold2:#d4a017;
  --white:#f8f5ef; --card:#1a1a1a; --card2:#222; --border:#2e2e2e;
  --muted:#777; --success:#22c55e; --info:#3b82f6;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:var(--black)!important;color:var(--white)!important;}
h1,h2,h3{font-family:'Playfair Display',serif!important;}
h1{color:var(--gold)!important;font-size:2.2rem!important;}
h2{color:var(--red)!important;}
h3{color:var(--gold2)!important;}

/* sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d0d0d 0%,#1a0000 100%)!important;border-right:2px solid var(--red)!important;}
[data-testid="stSidebar"] *{color:var(--white)!important;}

/* metrics */
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:16px!important;}
[data-testid="stMetricValue"]{color:var(--gold)!important;font-size:1.8rem!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;}

/* progress */
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,var(--red),var(--gold))!important;}

/* buttons */
.stButton>button{background:linear-gradient(135deg,var(--red),#8b0000)!important;color:var(--white)!important;border:none!important;border-radius:8px!important;font-weight:600!important;transition:all .15s ease!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(204,0,0,.4)!important;}
.gold-btn .stButton>button{background:linear-gradient(135deg,var(--gold),var(--gold2))!important;color:var(--black)!important;}
.green-btn .stButton>button{background:linear-gradient(135deg,#16a34a,#166534)!important;}
.ghost-btn .stButton>button{background:transparent!important;border:1px solid var(--border)!important;color:var(--muted)!important;}

/* tabs */
[data-testid="stTabs"] button{color:var(--muted)!important;font-weight:500!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--gold)!important;border-bottom:2px solid var(--gold)!important;}

/* inputs */
[data-testid="stSelectbox"]>div,[data-testid="stTextInput"]>div>div,[data-testid="stTextArea"]>div>div{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--white)!important;border-radius:8px!important;}

/* custom cards */
.gmc-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 24px;margin-bottom:14px;}
.gmc-card.gold{border-left:4px solid var(--gold);}
.gmc-card.red{border-left:4px solid var(--red);}
.gmc-card.green{border-left:4px solid var(--success);}
.gmc-card.flag{background:linear-gradient(135deg,#1a1a1a 60%,#1a0000 100%);border:1px solid var(--red);}

/* auth form */
.auth-box{max-width:440px;margin:60px auto;background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px;}
.auth-logo{text-align:center;font-size:3rem;margin-bottom:8px;}
.auth-title{text-align:center;font-family:'Playfair Display',serif;font-size:1.6rem;color:var(--gold);margin-bottom:4px;}
.auth-sub{text-align:center;color:var(--muted);font-size:.88rem;margin-bottom:28px;}

/* mantra */
.mantra-box{background:linear-gradient(135deg,#1a0a00,#1a1a00);border:1px solid var(--gold);border-radius:14px;padding:22px 28px;text-align:center;font-size:1.1rem;font-style:italic;color:var(--gold);font-family:'Playfair Display',serif;margin-bottom:22px;}

/* day node (road map) */
.day-node{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:14px 18px;margin-bottom:8px;transition:border-color .2s;}
.day-node.done{border-left:4px solid var(--success);}
.day-node.current{border-left:4px solid var(--gold);background:#1a1800;}
.day-node.locked{opacity:.45;pointer-events:none;}
.node-num{background:var(--red);color:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0;}
.node-num.done{background:var(--success);}
.node-num.locked{background:#333;}

/* leaderboard */
.lb-row{display:flex;align-items:center;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 18px;margin-bottom:8px;gap:12px;}
.lb-rank{font-size:1.3rem;width:32px;flex-shrink:0;}
.lb-name{flex:1;font-weight:600;}
.lb-xp{color:var(--gold);font-weight:700;}

/* game cards */
.game-card{background:linear-gradient(135deg,#1a1a1a,#0d0d0d);border:1px solid var(--gold);border-radius:16px;padding:28px;text-align:center;cursor:pointer;transition:all .2s;}
.game-card:hover{border-color:var(--red);transform:translateY(-4px);box-shadow:0 12px 32px rgba(204,0,0,.25);}

/* admin badge */
.admin-badge{display:inline-block;background:var(--gold);color:var(--black);border-radius:6px;padding:2px 10px;font-size:.75rem;font-weight:700;letter-spacing:.04em;}

/* tag */
.phase-tag{display:inline-block;background:var(--red);color:#fff;border-radius:6px;padding:2px 10px;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;}

div[data-testid="column"]{padding:6px!important;}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ════════════════════════════════════════════════════════════════════
defaults = {
    "logged_in": False, "user": None, "is_admin": False,
    "current_page": "home", "game_state": {},
    "ai_messages": [], "completed_days": set(),
    "daily_task_state": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Re-load completed days from DB user record
def sync_progress_from_db():
    if st.session_state.user:
        raw = str(st.session_state.user.get("CompletedDays", ""))
        if raw:
            try:
                st.session_state.completed_days = set(json.loads(raw))
            except Exception:
                st.session_state.completed_days = set()

# ════════════════════════════════════════════════════════════════════
#  STATIC DATA  —  Fallback content when no GSheet configured
# ════════════════════════════════════════════════════════════════════
MANTRAS = [
    '"Sprache ist nicht nur Kommunikation — sie ist Identität." 🇩🇪',
    '"Every German word you learn is a door to a new world."',
    '"Fehler machen ist menschlich. Aufhören ist optional."',
    '"Du schaffst das! One day at a time, one word at a time."',
    '"Repetition is the mother of mastery. Wiederholen = Meistern."',
    '"Ein Schritt nach dem anderen führt zum Ziel."',
]

PHASES = {
    "🏗️ Foundation": list(range(1, 31)),
    "🧱 Construction": list(range(31, 61)),
    "⚡ Activation": list(range(61, 91)),
}

SAMPLE_VOCAB = {
    "foundation": [
        ("Hallo","Hello"),("Danke","Thank you"),("Bitte","Please"),
        ("Ja","Yes"),("Nein","No"),("Haus","House"),("Auto","Car"),
        ("Wasser","Water"),("Brot","Bread"),("Mann","Man"),
    ],
    "construction": [
        ("Kaufen","To buy"),("Sprechen","To speak"),("Lesen","To read"),
        ("Schreiben","To write"),("Lernen","To learn"),("Arbeit","Work"),
        ("Familie","Family"),("Schule","School"),("Zeit","Time"),("Geld","Money"),
    ],
    "activation": [
        ("Tatsächlich","Actually"),("Trotzdem","Nevertheless"),("Obwohl","Although"),
        ("Deshalb","Therefore"),("Bereits","Already"),("Eigentlich","Actually/Basically"),
        ("Allerdings","However"),("Immerhin","At least"),("Schließlich","Finally"),("Übrigens","By the way"),
    ],
}

PHONETICS_LAB = [
    {"sym":"r",  "name":"Das R",  "desc":"Guttural — like gargling softly",      "yt":"oRpSJXMJUDg"},
    {"sym":"ch", "name":"Das CH", "desc":"'ich' soft vs 'ach' hard — position!",  "yt":"pN3Aqs9BGLM"},
    {"sym":"ä",  "name":"Das Ä",  "desc":"Like English 'air' but shorter",        "yt":"XbiBS5YIQB0"},
    {"sym":"ö",  "name":"Das Ö",  "desc":"Round lips, say 'e' — French 'eu'",     "yt":"XbiBS5YIQB0"},
    {"sym":"ü",  "name":"Das Ü",  "desc":"Round lips, say 'i' — French 'u'",      "yt":"XbiBS5YIQB0"},
    {"sym":"ß",  "name":"Das ß",  "desc":"Sharp SS — never starts a word",        "yt":"oRpSJXMJUDg"},
]

RESOURCES = [
    {"cat":"📺 Video", "name":"Nicos Weg — DW A1 Series",          "url":"https://www.dw.com/de/nicos-weg/s-52164"},
    {"cat":"📺 Video", "name":"Easy German — Street Interviews",    "url":"https://www.youtube.com/@EasyGerman"},
    {"cat":"📺 Video", "name":"Deutsch für Euch — Grammar",         "url":"https://www.youtube.com/@DeutschFuerEuch"},
    {"cat":"🃏 Anki",  "name":"AnkiWeb — Sync Your Decks",          "url":"https://ankiweb.net"},
    {"cat":"🃏 Anki",  "name":"German Core 2k Shared Deck",         "url":"https://ankiweb.net/shared/info/1558798271"},
    {"cat":"🔊 Audio", "name":"YouGlish German",                    "url":"https://youglish.com/german"},
    {"cat":"🔊 Audio", "name":"Slow German Podcast",                "url":"https://slowgerman.com"},
    {"cat":"🔊 Audio", "name":"Forvo — Native Pronunciations",      "url":"https://forvo.com/languages/de/"},
    {"cat":"📖 Read",  "name":"DW Learn German Articles",           "url":"https://www.dw.com/en/learn-german/s-2053"},
    {"cat":"🛠️ Tools", "name":"dict.cc — Best Bilingual Dictionary", "url":"https://www.dict.cc"},
    {"cat":"🛠️ Tools", "name":"Reverso Context",                    "url":"https://context.reverso.net"},
    {"cat":"🛠️ Tools", "name":"LanguageTool — Grammar Checker",     "url":"https://languagetool.org"},
]

CULTURAL_DROPS = [
    {"w":1,"title":"Pünktlichkeit 🕐","body":"Germans value punctuality above almost everything. Being 5 min late is rude — 5 min early is respectful."},
    {"w":2,"title":"Kaffee & Kuchen ☕","body":"Sunday coffee and cake (Kaffee und Kuchen) is a sacred family tradition."},
    {"w":3,"title":"Recycling Culture ♻️","body":"Germany has one of the world's best recycling systems — Pfand (bottle deposits) make sustainability everyone's business."},
    {"w":4,"title":"Brot & Wurst 🥖","body":"Germany has 3,200+ bread varieties. Bread is emotional — 'Heimweh' often starts with missing Brot."},
]

# ════════════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════════════
def get_phase(day: int) -> str:
    if day <= 30:  return "Foundation"
    if day <= 60:  return "Construction"
    return "Activation"

def get_vocab_for_user() -> list:
    phase = get_phase(len(st.session_state.completed_days) + 1).lower()
    return SAMPLE_VOCAB.get(phase, SAMPLE_VOCAB["foundation"])

def day_is_unlocked(day: int) -> bool:
    if day == 1: return True
    return (day - 1) in st.session_state.completed_days

def compute_streak(done: set) -> int:
    if not done: return 0
    streak, d = 0, max(done)
    while d in done:
        streak += 1; d -= 1
    return streak

def user_xp() -> int:
    if st.session_state.user:
        return int(st.session_state.user.get("XP", 0)) + len(st.session_state.completed_days) * 20
    return len(st.session_state.completed_days) * 20

def save_progress():
    """Persist progress to Google Sheet."""
    if st.session_state.user:
        xp = user_xp()
        streak = compute_streak(st.session_state.completed_days)
        days_json = json.dumps(list(st.session_state.completed_days))
        update_user_xp(st.session_state.user["Email"], xp, streak, days_json)

def is_admin() -> bool:
    return st.session_state.is_admin

# ════════════════════════════════════════════════════════════════════
#  AI COPILOT (wrapped via ai_engine)
# ════════════════════════════════════════════════════════════════════
# We now delegate all AI logic to ai_engine (Groq) imported above.  
# The functions below simply call those helpers, ensuring the rest of
# the codebase can continue using the same names.

def ai_correct_german(text: str) -> str:
    """Wrapper around ai_grammar_fixer from ai_engine."""
    return ai_grammar_fixer(text)


def ai_chat(messages: list, user_msg: str) -> str:
    """Wrapper around engine_chat imported from ai_engine."""
    return engine_chat(messages, user_msg)

# ════════════════════════════════════════════════════════════════════
#  UI COMPONENTS
# ════════════════════════════════════════════════════════════════════
def render_xp_bar():
    done = len(st.session_state.completed_days)
    xp = user_xp()
    streak = compute_streak(st.session_state.completed_days)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📅 Day", f"{min(done+1,90)}/90")
    c2.metric("⭐ XP",  xp)
    c3.metric("🔥 Streak", f"{streak}d")
    c4.metric("✅ Done", done)

# ════════════════════════════════════════════════════════════════════
#  PAGES
# ════════════════════════════════════════════════════════════════════

# ── AUTH PAGE ────────────────────────────────────────────────────────
def page_auth():
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.markdown("""
        <div class='auth-logo'>🇩🇪</div>
        <div class='auth-title'>German Mastery Camp</div>
        <div class='auth-sub'>{subtitle}</div>
        """.format(subtitle=tr("home_subtitle")), unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔑 " + tr("sign_in"), "🆕 " + tr("create_account")])

        with tab_login:
            email = st.text_input(tr("email"), key="li_email", placeholder="you@example.com")
            pw    = st.text_input(tr("password"), type="password", key="li_pw")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(tr("sign_in") + " →", key="btn_login", use_container_width=True):
                    if not email or not pw:
                        st.error(tr("please_fill"))
                    else:
                        gc = get_gsheet_client()
                        if gc is None:
                            # demo mode
                            st.session_state.logged_in = True
                            st.session_state.user = {"Name": email.split("@")[0].title(), "Email": email, "XP": 0, "Streak": 0, "CompletedDays": ""}
                            st.rerun()
                        else:
                            user = login_user(email, pw)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user = user
                                sync_progress_from_db()
                                st.rerun()
                            else:
                                st.error(tr("invalid_credentials"))
            with col_b:
                admin_pw_try = st.text_input(tr("admin_login"), type="password", key="admin_pw_inp")
                if st.button(tr("admin_login"), key="btn_admin"):
                    correct = st.secrets.get("admin_password", "admin1234")
                    if admin_pw_try == correct:
                        st.session_state.logged_in = True
                        st.session_state.is_admin  = True
                        st.session_state.user = {"Name":"Admin","Email":"admin@camp.de","XP":9999,"Streak":90,"CompletedDays":""}
                        st.rerun()
                    else:
                        st.error(tr("wrong_password"))

        with tab_register:
            name  = st.text_input(tr("full_name"), key="reg_name")
            email2 = st.text_input(tr("email"), key="reg_email")
            pw2   = st.text_input(tr("password"), type="password", key="reg_pw")
            pw2c  = st.text_input(tr("password_confirm"), type="password", key="reg_pw2")
            if st.button(tr("create_account") + " →", key="btn_reg", use_container_width=True):
                if not all([name, email2, pw2, pw2c]):
                    st.error(tr("please_fill"))
                elif pw2 != pw2c:
                    st.error(tr("password_mismatch"))
                elif len(pw2) < 6:
                    st.error(tr("password_length"))
                else:
                    gc = get_gsheet_client()
                    if gc is None:
                        st.session_state.logged_in = True
                        st.session_state.user = {"Name":name,"Email":email2,"XP":0,"Streak":0,"CompletedDays":""}
                        st.success(tr("welcome_demo"))
                        time.sleep(1); st.rerun()
                    else:
                        if register_user(name, email2, pw2):
                            st.success(tr("account_created"))
                        else:
                            st.error(tr("email_exists"))

        st.markdown("""
        <div style='text-align:center; margin-top:20px; color:#555; font-size:.82rem;'>
            Open registration — anyone can join free 🎉
        </div>
        """, unsafe_allow_html=True)


# ── HOME ─────────────────────────────────────────────────────────────
def page_home():
    name = st.session_state.user.get("Name", "Learner")
    st.markdown(f"# 🇩🇪 Willkommen, {name}!")
    st.markdown("### *Learning is living — not just memorizing.*")

    mantra = MANTRAS[datetime.date.today().timetuple().tm_yday % len(MANTRAS)]
    st.markdown(f'<div class="mantra-box">💬 Mantra of the Day<br><br>{mantra}</div>', unsafe_allow_html=True)

    render_xp_bar()

    st.markdown("---")
    st.markdown("## 🗺️ Your 90-Day Journey")
    cols = st.columns(3)
    for i, (phase, days) in enumerate(PHASES.items()):
        done_here = len([d for d in days if d in st.session_state.completed_days])
        pct = done_here / len(days)
        with cols[i]:
            st.markdown(f"""
            <div class='gmc-card {"gold" if i==0 else "red" if i==1 else "green"}'>
                <div style='font-size:1.4rem'>{phase.split()[0]}</div>
                <div style='font-weight:700;margin:4px 0;'>{" ".join(phase.split()[1:])}</div>
                <div style='color:#888;font-size:.82rem;margin-bottom:10px;'>Days {days[0]}–{days[-1]}</div>
                <div style='color:#f5c518;font-size:1.6rem;font-weight:700;'>{done_here}/{len(days)}</div>
                <div style='color:#888;font-size:.8rem;'>days completed</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct)

    # Weekly cultural drop
    week_num = min((len(st.session_state.completed_days) // 7), 3)
    drop = CULTURAL_DROPS[week_num]
    st.markdown("---")
    st.markdown("## 🌍 This Week's Cultural Drop")
    st.markdown(f"""
    <div class='gmc-card flag'>
        <div style='font-size:1.2rem;font-weight:700;color:#f5c518;margin-bottom:8px;'>{drop['title']}</div>
        <p style='line-height:1.8;color:#ccc;'>{drop['body']}</p>
    </div>
    """, unsafe_allow_html=True)


# ── ROADMAP ──────────────────────────────────────────────────────────
def page_roadmap():
    st.markdown("# 🗺️ Learning Roadmap")
    st.markdown("Complete each day to unlock the next. 🔒 = locked, ✅ = done, 🟡 = today")
    st.markdown("<br>", unsafe_allow_html=True)

    search = st.text_input("🔍 Search topic", placeholder="Type to filter days…", label_visibility="collapsed")

    for phase_name, days in PHASES.items():
        st.markdown(f"### {phase_name}")
        for day in days:
            is_done    = day in st.session_state.completed_days
            is_current = day_is_unlocked(day) and not is_done
            is_locked  = not day_is_unlocked(day)
            phase_str  = get_phase(day)

            # Load from GSheet if available
            content_df = load_sheet("Content")
            if not content_df.empty and "Day_Number" in content_df.columns:
                row = content_df[content_df["Day_Number"].astype(str) == str(day)]
                topic = row.iloc[0].get("Topic","") if not row.empty else f"Day {day} — {phase_str}"
            else:
                topic = f"Day {day} — {phase_str}"

            if search and search.lower() not in topic.lower():
                continue

            status_class = "done" if is_done else "current" if is_current else "locked"
            num_class    = "done" if is_done else "locked" if is_locked else ""
            icon = "✅" if is_done else "🔒" if is_locked else "▶"

            col_node, col_btn = st.columns([5,1])
            with col_node:
                st.markdown(f"""
                <div class='day-node {status_class}'>
                    <div class='node-num {num_class}'>{day}</div>
                    <div>
                        <div style='font-weight:600;font-size:.95rem;'>{topic}</div>
                        <div style='color:#666;font-size:.78rem;'>
                            {icon} {("Completed" if is_done else "Locked" if is_locked else "Available")}
                            &nbsp;·&nbsp; {phase_str}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if is_current or is_done:
                    st.markdown("<div class='gold-btn'>", unsafe_allow_html=True)
                    if st.button("Open" if is_current else "Review", key=f"open_day_{day}"):
                        st.session_state.current_page = "daily"
                        st.session_state.selected_day = day
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ── DAILY DASHBOARD ──────────────────────────────────────────────────
def page_daily():
    sel = st.session_state.get("selected_day", len(st.session_state.completed_days) + 1)
    sel = max(1, min(sel, 90))

    st.markdown(f"# 📅 Day {sel} — Daily Mission")

    if not day_is_unlocked(sel):
        st.warning("🔒 This day is locked. Complete the previous day first.")
        return

    phase_str = get_phase(sel)
    st.markdown(f'<span class="phase-tag">{phase_str}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Load day content from sheet or use defaults
    content_df = load_sheet("Content")
    day_row = {}
    if not content_df.empty and "Day_Number" in content_df.columns:
        r = content_df[content_df["Day_Number"].astype(str) == str(sel)]
        if not r.empty:
            day_row = r.iloc[0].to_dict()

    topic         = day_row.get("Topic", f"Day {sel} Content")
    video_id      = day_row.get("Video_ID", "")
    anki_task     = day_row.get("Anki_Task", "Review your Anki deck and add 10 new cards (30 min)")
    pronunciation = day_row.get("Pronunciation_Task", "Practice 3 difficult sounds on YouGlish (30 min)")
    writing_task  = day_row.get("Writing_Task", "Write 5 sentences using today's vocabulary (30 min)")
    reading_text  = day_row.get("Reading_Text", "")
    arabic_link   = day_row.get("Video_Link_Arabic", "")

    st.markdown(f"### 📖 {topic}")

    # Foundation Bridge (Days 1-14)
    if sel <= 14 and arabic_link:
        st.markdown(f"""
        <div class='gmc-card gold'>
            <strong>🌉 Foundation Bridge — Arabic Support</strong>
            <p style='margin-top:8px;'>Watch today's Arabic explanation before diving in:</p>
            <a href='{arabic_link}' target='_blank' style='color:#f5c518;font-weight:600;text-decoration:none;'>📺 Arabic Bridge Video →</a>
        </div>
        """, unsafe_allow_html=True)

    # YouTube Player
    if video_id:
        st.markdown("### 📺 Today's Video")
        st.markdown(f"""
        <div style='position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;margin-bottom:16px;'>
            <iframe style='position:absolute;top:0;left:0;width:100%;height:100%;border:none;border-radius:12px;'
                src='https://www.youtube.com/embed/{video_id}?rel=0' allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        nicos_url = f"https://www.dw.com/de/nicos-weg/s-52164?episode={sel}"
        st.markdown(f"""
        <div class='gmc-card red'>
            <strong>📺 Nicos Weg — Episode {sel}</strong>
            <p style='margin-top:8px;color:#ccc;'>Follow Nico and absorb German naturally.</p>
            <a href='{nicos_url}' target='_blank' style='color:#f5c518;font-weight:600;text-decoration:none;'>🎬 Watch on DW →</a>
        </div>
        """, unsafe_allow_html=True)

    # Reading text
    if reading_text:
        with st.expander("📖 Today's Reading Text"):
            st.markdown(f"<div style='line-height:1.9;'>{reading_text}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✅ 120-Minute Mission Checklist")

    day_key = f"day_{sel}"
    if day_key not in st.session_state.daily_task_state:
        st.session_state.daily_task_state[day_key] = {"anki":False,"nicos":False,"pronunciation":False,"writing":False}

    t = st.session_state.daily_task_state[day_key]
    c1, c2 = st.columns(2)
    with c1:
        t["anki"]         = st.checkbox(f"🃏 {anki_task}",         value=t["anki"],         key=f"t_anki_{sel}")
        t["nicos"]        = st.checkbox("📺 Watch Nicos Weg + shadow (30 min)", value=t["nicos"], key=f"t_nicos_{sel}")
    with c2:
        t["pronunciation"]= st.checkbox(f"🔊 {pronunciation}",     value=t["pronunciation"], key=f"t_pro_{sel}")
        t["writing"]      = st.checkbox(f"✍️ {writing_task}",       value=t["writing"],       key=f"t_write_{sel}")

    st.session_state.daily_task_state[day_key] = t
    done_count = sum(t.values())

    st.markdown(f"**Progress: {done_count}/4 tasks**")
    st.progress(done_count / 4)

    if done_count == 4 and sel not in st.session_state.completed_days:
        st.markdown("<div class='gold-btn'>", unsafe_allow_html=True)
        if st.button(f"🏆 Complete Day {sel} — Earn 20 XP ⭐", key=f"complete_{sel}"):
            st.session_state.completed_days.add(sel)
            save_progress()
            st.balloons()
            st.success(f"🎉 Wunderbar! Day {sel} complete! +20 XP earned!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    elif sel in st.session_state.completed_days:
        st.success(f"✅ Day {sel} already completed! Ausgezeichnet! 🌟")

    # Quick links
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<a href="https://youglish.com/german" target="_blank" class="resource-link" style="display:block;background:#1a1a1a;border:1px solid #2e2e2e;border-radius:10px;padding:14px 18px;color:white;text-decoration:none;">🎙️ <strong>YouGlish German</strong><br><span style="color:#555;font-size:.82rem;">Hear any word by native speakers</span></a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a href="https://ankiweb.net" target="_blank" class="resource-link" style="display:block;background:#1a1a1a;border:1px solid #2e2e2e;border-radius:10px;padding:14px 18px;color:white;text-decoration:none;">🃏 <strong>AnkiWeb</strong><br><span style="color:#555;font-size:.82rem;">Review flashcard decks online</span></a>', unsafe_allow_html=True)


# ── AI COPILOT ───────────────────────────────────────────────────────
def page_ai_copilot():
    st.markdown("# 🤖 AI Copilot — Klaus")
    st.markdown("*Your personal German tutor, available 24/7.*")
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💬 Chat with Klaus", "✍️ Grammar Fixer"])

    with tab1:
        # Chat history display
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.ai_messages:
                role_label = "🧑 You" if msg["role"] == "user" else "🤖 Klaus"
                bg = "#1a1a1a" if msg["role"] == "user" else "#1a0a00"
                border = "#2e2e2e" if msg["role"] == "user" else "#f5c518"
                st.markdown(f"""
                <div style='background:{bg};border:1px solid {border};border-radius:10px;
                            padding:12px 16px;margin-bottom:10px;'>
                    <div style='color:#888;font-size:.75rem;margin-bottom:4px;'>{role_label}</div>
                    <div style='line-height:1.7;white-space:pre-wrap;'>{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

        user_input = st.text_input("Ask Klaus anything about German…", key="chat_input", placeholder="z.B. What is the difference between 'seit' and 'vor'?")
        c1, c2 = st.columns([3,1])
        with c1:
            if st.button("Send →", key="send_chat"):
                if user_input.strip():
                    with st.spinner("Klaus is thinking…"):
                        reply = ai_chat(st.session_state.ai_messages, user_input)
                    st.session_state.ai_messages.append({"role":"user","content":user_input})
                    st.session_state.ai_messages.append({"role":"assistant","content":reply})
                    st.rerun()
        with c2:
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.ai_messages = []
                st.rerun()

    with tab2:
        st.markdown("### ✍️ AI Grammar Fixer")
        st.markdown("Write your German text below — Klaus will correct it and explain every mistake.")

        user_text = st.text_area("Your German text", height=120, key="grammar_input",
                                  placeholder="Ich bin gehen zum Markt gestern...")
        if st.button("🔍 Analyze & Fix", key="grammar_fix"):
            if user_text.strip():
                with st.spinner("Analyzing your German…"):
                    result = ai_correct_german(user_text)
                st.markdown("---")
                st.markdown("### 📝 Klaus's Feedback")
                st.markdown(f"""
                <div class='gmc-card gold'>
                    <div style='line-height:1.9; white-space:pre-wrap;'>{result}</div>
                </div>
                """, unsafe_allow_html=True)
                # Save submission
                if st.session_state.user:
                    write_row("Submissions", [
                        st.session_state.user.get("Name",""),
                        st.session_state.user.get("Email",""),
                        user_text, result,
                        datetime.datetime.now().isoformat()
                    ])
            else:
                st.warning("Please write some German text first.")


# ── MINI GAMES ───────────────────────────────────────────────────────
def page_games():
    st.markdown("# 🎮 Mini Games")
    st.markdown("*Learn through play. Earn XP for every game you complete.*")
    st.markdown("<br>", unsafe_allow_html=True)

    game = st.session_state.game_state.get("active_game")

    if game is None:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""<div class='game-card'>
                <div style='font-size:2.5rem;margin-bottom:10px;'>🃏</div>
                <div style='font-weight:700;font-size:1.1rem;color:#f5c518;'>Flashcard Quiz</div>
                <div style='color:#888;font-size:.85rem;margin-top:8px;'>Test your vocabulary recall</div>
                <div style='color:#cc0000;font-size:.8rem;margin-top:12px;'>+10 XP per round</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Play →", key="start_flash"):
                vocab = get_vocab_for_user()
                random.shuffle(vocab)
                st.session_state.game_state = {"active_game":"flashcard","vocab":vocab,"index":0,"score":0,"total":min(8,len(vocab)),"answered":False}
                st.rerun()

        with c2:
            st.markdown("""<div class='game-card'>
                <div style='font-size:2.5rem;margin-bottom:10px;'>🔗</div>
                <div style='font-weight:700;font-size:1.1rem;color:#f5c518;'>Word Match</div>
                <div style='color:#888;font-size:.85rem;margin-top:8px;'>Match German words to meanings</div>
                <div style='color:#cc0000;font-size:.8rem;margin-top:12px;'>+15 XP per round</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Play →", key="start_match"):
                vocab = get_vocab_for_user()
                random.shuffle(vocab)
                pairs = vocab[:6]
                st.session_state.game_state = {"active_game":"wordmatch","pairs":pairs,"selected_de":None,"selected_en":None,"matched":[],"errors":0}
                st.rerun()

        with c3:
            st.markdown("""<div class='game-card'>
                <div style='font-size:2.5rem;margin-bottom:10px;'>🔀</div>
                <div style='font-weight:700;font-size:1.1rem;color:#f5c518;'>Sentence Scramble</div>
                <div style='color:#888;font-size:.85rem;margin-top:8px;'>Re-order words into correct German</div>
                <div style='color:#cc0000;font-size:.8rem;margin-top:12px;'>+20 XP per round</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Play →", key="start_scramble"):
                sentences = [
                    ("Ich lerne jeden Tag Deutsch.", ["jeden","Deutsch.","lerne","Ich","Tag"]),
                    ("Er geht morgen in die Schule.", ["in","geht","Er","Schule.","morgen","die"]),
                    ("Wir essen zusammen am Abend.", ["Wir","am","essen","Abend.","zusammen"]),
                ]
                s = random.choice(sentences)
                scrambled = s[1][:]
                random.shuffle(scrambled)
                st.session_state.game_state = {"active_game":"scramble","correct":s[0],"words":scrambled,"answer":"","done":False}
                st.rerun()

    # ── Flashcard game ──
    elif game == "flashcard":
        gs = st.session_state.game_state
        idx = gs["index"]
        if idx >= gs["total"]:
            xp_earned = gs["score"] * 10
            st.success(f"🎉 Game Over! Score: {gs['score']}/{gs['total']} | +{xp_earned} XP")
            if st.session_state.user:
                st.session_state.user["XP"] = int(st.session_state.user.get("XP",0)) + xp_earned
            if st.button("Play Again"):
                st.session_state.game_state = {}; st.rerun()
            return

        de_word, en_word = gs["vocab"][idx]
        all_vocab = get_vocab_for_user()
        wrong_options = [w[1] for w in all_vocab if w[1] != en_word]
        random.shuffle(wrong_options)
        options = ([en_word] + wrong_options[:3])
        random.shuffle(options)

        st.markdown(f"### 🃏 Card {idx+1}/{gs['total']}")
        st.markdown(f'<div class="gmc-card gold" style="text-align:center;"><div style="font-size:2.5rem;font-weight:700;color:#f5c518;">{de_word}</div><div style="color:#888;margin-top:6px;">What does this mean?</div></div>', unsafe_allow_html=True)
        st.markdown(f"Score: {gs['score']} ⭐ | Progress: {idx}/{gs['total']}")
        st.progress(idx / gs["total"])
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(2)
        for ci, opt in enumerate(options):
            with cols[ci % 2]:
                if st.button(opt, key=f"flash_opt_{ci}_{idx}"):
                    if opt == en_word:
                        gs["score"] += 1
                        st.success("✅ Richtig! (Correct!)")
                    else:
                        st.error(f"❌ Wrong! The answer was: **{en_word}**")
                    gs["index"] += 1
                    st.session_state.game_state = gs
                    time.sleep(0.5); st.rerun()

        if st.button("⬅ Exit Game", key="exit_flash"):
            st.session_state.game_state = {}; st.rerun()

    # ── Word Match game ──
    elif game == "wordmatch":
        gs = st.session_state.game_state
        matched = gs["matched"]
        pairs = gs["pairs"]

        st.markdown("### 🔗 Word Match")
        st.markdown("Click a German word then its English meaning to match them.")
        st.markdown(f"Matched: {len(matched)//2}/{len(pairs)} | Errors: {gs['errors']}")

        if len(matched) == len(pairs) * 2:
            xp = max(0, 15 - gs["errors"]) * 3
            st.success(f"🎉 All matched! Errors: {gs['errors']} | +{xp} XP")
            if st.session_state.user:
                st.session_state.user["XP"] = int(st.session_state.user.get("XP",0)) + xp
            if st.button("Play Again"):
                st.session_state.game_state = {}; st.rerun()
            return

        de_words = [p[0] for p in pairs]
        en_words = [p[1] for p in pairs]
        random.seed(42)
        random.shuffle(en_words)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🇩🇪 German**")
            for w in de_words:
                if w in matched: st.markdown(f"~~{w}~~ ✅")
                else:
                    selected = gs.get("selected_de") == w
                    style = "background:#1a0800;border:2px solid #f5c518;" if selected else ""
                    if st.button(w, key=f"de_{w}"):
                        gs["selected_de"] = w
                        if gs.get("selected_en"):
                            correct_en = dict(pairs).get(w)
                            if gs["selected_en"] == correct_en:
                                gs["matched"] += [w, gs["selected_en"]]
                            else:
                                gs["errors"] += 1
                            gs["selected_de"] = None; gs["selected_en"] = None
                        st.session_state.game_state = gs; st.rerun()
        with c2:
            st.markdown("**🇬🇧 English**")
            for w in en_words:
                if w in matched: st.markdown(f"~~{w}~~ ✅")
                else:
                    if st.button(w, key=f"en_{w}"):
                        gs["selected_en"] = w
                        if gs.get("selected_de"):
                            correct_en = dict(pairs).get(gs["selected_de"])
                            if w == correct_en:
                                gs["matched"] += [gs["selected_de"], w]
                            else:
                                gs["errors"] += 1
                            gs["selected_de"] = None; gs["selected_en"] = None
                        st.session_state.game_state = gs; st.rerun()

        if st.button("⬅ Exit", key="exit_match"):
            st.session_state.game_state = {}; st.rerun()

    # ── Scramble game ──
    elif game == "scramble":
        gs = st.session_state.game_state
        st.markdown("### 🔀 Sentence Scramble")
        st.markdown("Rearrange these words into the correct German sentence:")
        st.markdown(f"""<div class='gmc-card gold'><strong style='font-size:1.1rem;'>Words: {" · ".join(gs['words'])}</strong></div>""", unsafe_allow_html=True)

        answer = st.text_input("Your answer:", key="scramble_ans", placeholder="Type the sentence...")
        if st.button("✅ Check Answer", key="check_scramble"):
            if answer.strip().lower() == gs["correct"].lower():
                st.success("🎉 Perfekt! Correct! +20 XP")
                if st.session_state.user:
                    st.session_state.user["XP"] = int(st.session_state.user.get("XP",0)) + 20
                gs["done"] = True; st.session_state.game_state = gs
            else:
                st.error(f"❌ Not quite. Correct: **{gs['correct']}**")

        if gs.get("done") or st.button("⬅ Exit", key="exit_scramble"):
            st.session_state.game_state = {}; st.rerun()


# ── LEADERBOARD ──────────────────────────────────────────────────────
def page_leaderboard():
    st.markdown("# 🏆 Leaderboard")
    st.markdown("*The fire of competition keeps the flame of learning alive.*")
    st.markdown("<br>", unsafe_allow_html=True)

    users_df = load_sheet("Users")

    # Build leaderboard data
    if not users_df.empty and "Name" in users_df.columns:
        lb_data = []
        for _, row in users_df.iterrows():
            try:
                days = len(json.loads(str(row.get("CompletedDays","[]"))))
            except Exception:
                days = 0
            lb_data.append({
                "Name": row.get("Name","?"),
                "XP":   int(row.get("XP", 0)) + days * 20,
                "Streak": int(row.get("Streak", 0)),
                "Days": days,
            })
        # Add current user if not already in DB
        my_name = st.session_state.user.get("Name","")
        if not any(u["Name"] == my_name for u in lb_data):
            lb_data.append({"Name": my_name, "XP": user_xp(), "Streak": compute_streak(st.session_state.completed_days), "Days": len(st.session_state.completed_days)})
    else:
        # Demo leaderboard
        lb_data = [
            {"Name":"Sara",    "XP":320, "Streak":14, "Days":16},
            {"Name":"Ahmed",   "XP":280, "Streak":11, "Days":14},
            {"Name":"Layla",   "XP":240, "Streak":9,  "Days":12},
            {"Name":"Mohamed", "XP":180, "Streak":7,  "Days":9},
            {"Name": st.session_state.user.get("Name","You"), "XP": user_xp(), "Streak": compute_streak(st.session_state.completed_days), "Days": len(st.session_state.completed_days)},
        ]

    tab1, tab2 = st.tabs(["⭐ XP Ranking", "🔥 Streak Ranking"])
    medals = ["🥇","🥈","🥉"] + ["🏅"]*50
    my_name = st.session_state.user.get("Name","")

    with tab1:
        sorted_lb = sorted(lb_data, key=lambda x: x["XP"], reverse=True)
        for i, u in enumerate(sorted_lb):
            is_you = u["Name"] == my_name
            you_tag = "<span style='background:#f5c518;color:#000;border-radius:4px;padding:1px 8px;font-size:.72rem;font-weight:700;margin-left:6px;'>YOU</span>" if is_you else ""
            border = "border:2px solid #f5c518!important;" if is_you else ""
            st.markdown(f"""<div class='lb-row' style='{border}'>
                <span class='lb-rank'>{medals[i]}</span>
                <span class='lb-name'>{u["Name"]}{you_tag}</span>
                <span style='color:#888;font-size:.82rem;margin-right:16px;'>🔥 {u["Streak"]}d</span>
                <span class='lb-xp'>⭐ {u["XP"]} XP</span>
            </div>""", unsafe_allow_html=True)

    with tab2:
        sorted_streak = sorted(lb_data, key=lambda x: x["Streak"], reverse=True)
        for i, u in enumerate(sorted_streak):
            is_you = u["Name"] == my_name
            you_tag = "<span style='background:#cc0000;color:#fff;border-radius:4px;padding:1px 8px;font-size:.72rem;font-weight:700;margin-left:6px;'>YOU</span>" if is_you else ""
            border = "border:2px solid #cc0000!important;" if is_you else ""
            st.markdown(f"""<div class='lb-row' style='{border}'>
                <span class='lb-rank'>{medals[i]}</span>
                <span class='lb-name'>{u["Name"]}{you_tag}</span>
                <span class='lb-xp'>🔥 {u["Streak"]} days</span>
            </div>""", unsafe_allow_html=True)


# ── PHONETICS LAB ────────────────────────────────────────────────────
def page_phonetics():
    st.markdown("# 🔬 Phonetics Lab")
    st.markdown("*Master the sounds that trip up Arabic speakers. Click any card to open its YouTube guide.*")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, ph in enumerate(PHONETICS_LAB):
        with cols[i % 3]:
            st.markdown(f"""
            <a href='https://www.youtube.com/watch?v={ph["yt"]}' target='_blank' style='text-decoration:none;'>
                <div class='game-card' style='cursor:pointer;'>
                    <div style='font-size:3rem;color:#f5c518;font-weight:900;font-family:"Playfair Display",serif;'>{ph["sym"]}</div>
                    <div style='font-weight:700;color:#fff;margin-top:8px;'>{ph["name"]}</div>
                    <div style='color:#888;font-size:.82rem;margin-top:4px;'>{ph["desc"]}</div>
                    <div style='color:#cc0000;font-size:.78rem;margin-top:10px;'>▶ YouTube Guide</div>
                </div>
            </a><br>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 👂 Minimal Pairs Practice")
    pairs = [
        ("bitten","bieten","to ask / to offer"), ("Hölle","Höhle","hell / cave"),
        ("Bach","Buch","stream / book"),         ("fahren","fähren","to drive / ferries"),
        ("suchen","kochen","to search / to cook"),("lesen","essen","to read / to eat"),
    ]
    for a, b, m in pairs:
        st.markdown(f"""
        <div style='display:flex;align-items:center;background:#1a1a1a;border:1px solid #2e2e2e;
                    border-radius:10px;padding:12px 18px;margin-bottom:8px;gap:12px;'>
            <span style='font-size:1.1rem;color:#f5c518;font-weight:700;width:90px;'>{a}</span>
            <span style='color:#555;'>vs</span>
            <span style='font-size:1.1rem;color:#cc0000;font-weight:700;width:90px;'>{b}</span>
            <span style='color:#888;font-size:.82rem;margin-left:auto;'>{m}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<br>
    <div class='gmc-card gold'>
        <p>Practice pronunciation with native speakers on YouGlish:</p>
        <a href='https://youglish.com/german' target='_blank' style='color:#f5c518;font-weight:700;text-decoration:none;'>🌐 Open YouGlish German →</a>
    </div>""", unsafe_allow_html=True)


# ── RESOURCES ────────────────────────────────────────────────────────
def page_resources():
    st.markdown("# 📚 Resource Library")
    st.markdown("<br>", unsafe_allow_html=True)
    cats = sorted(set(r["cat"] for r in RESOURCES))
    tabs = st.tabs(cats)
    for tab, cat in zip(tabs, cats):
        with tab:
            for r in [x for x in RESOURCES if x["cat"] == cat]:
                st.markdown(f"""
                <a href='{r["url"]}' target='_blank' style='display:block;background:#1a1a1a;border:1px solid #2e2e2e;border-radius:10px;padding:14px 18px;margin-bottom:10px;color:white;text-decoration:none;'>
                    <strong>{r["name"]}</strong><br>
                    <span style='color:#555;font-size:.8rem;'>{r["url"]}</span>
                </a>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
#  ADMIN PANEL
# ════════════════════════════════════════════════════════════════════
def page_admin():
    st.markdown('<span class="admin-badge">⚙️ ADMIN PANEL</span>', unsafe_allow_html=True)
    st.markdown("# Mission Control")
    st.markdown("*Manage content, monitor students, and control the camp.*")
    st.markdown("<br>", unsafe_allow_html=True)

    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "📋 Add Daily Mission", "👥 Students Overview", "🏆 Leaderboard Manager", "📊 Submissions"
    ])

    # ── Tab 1: Add Content ──
    with admin_tab1:
        st.markdown("### ➕ Add / Update Daily Mission")
        st.markdown("Fill in the fields and click Save. This writes directly to your Google Sheet.")

        c1, c2 = st.columns(2)
        with c1:
            day_num   = st.number_input("Day Number", 1, 90, 1, key="adm_day")
            phase     = st.selectbox("Phase", ["Foundation","Construction","Activation"], key="adm_phase")
            topic     = st.text_input("Topic / Title", key="adm_topic", placeholder="e.g. German Alphabet & Phonetics")
            video_id  = st.text_input("YouTube Video ID", key="adm_vid", placeholder="e.g. dQw4w9WgXcQ")
            arabic_link = st.text_input("Arabic Bridge Video URL (Days 1-14)", key="adm_arabic")
        with c2:
            anki_task   = st.text_area("Anki Task Description", height=80, key="adm_anki",  placeholder="Add 15 new vocab cards related to...")
            pron_task   = st.text_area("Pronunciation Task",    height=80, key="adm_pron",  placeholder="Practice ä, ö, ü on YouGlish for 10 min...")
            write_task  = st.text_area("Writing Task",          height=80, key="adm_write", placeholder="Write 5 sentences using today's vocabulary...")
            read_text   = st.text_area("Reading Text (optional)", height=80, key="adm_read")

        st.markdown("<div class='gold-btn'>", unsafe_allow_html=True)
        if st.button("💾 Save Mission to Google Sheet", key="adm_save"):
            row = [day_num, phase, topic, arabic_link, video_id, anki_task, pron_task, write_task, read_text]
            if write_row("Content", row):
                st.success(f"✅ Day {day_num} mission saved to Google Sheet!")
            else:
                st.error("Failed to write — check your Google Sheet connection.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Preview existing content
        st.markdown("---")
        st.markdown("### 📄 Current Content Sheet")
        content_df = load_sheet("Content")
        if not content_df.empty:
            st.dataframe(content_df, use_container_width=True)
        else:
            st.info("No content loaded yet. Add missions above or configure your Google Sheet.")

    # ── Tab 2: Students ──
    with admin_tab2:
        st.markdown("### 👥 Registered Students")
        users_df = load_sheet("Users")
        if not users_df.empty:
            # Remove password column for display
            display_df = users_df.drop(columns=["Password"], errors="ignore")
            st.dataframe(display_df, use_container_width=True)
            st.markdown(f"**Total students: {len(users_df)}**")

            # Status overview
            st.markdown("---")
            st.markdown("### 🔴🟢 Today's Completion Status")
            today_done = []
            today_missing = []
            for _, row in users_df.iterrows():
                try:
                    days = json.loads(str(row.get("CompletedDays","[]")))
                    current = len(days) + 1
                    if current in days:
                        today_done.append(row.get("Name","?"))
                    else:
                        today_missing.append(row.get("Name","?"))
                except Exception:
                    today_missing.append(row.get("Name","?"))

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ Done today:**")
                for n in today_done:
                    st.markdown(f"🟢 {n}")
            with c2:
                st.markdown("**⏳ Not done yet:**")
                for n in today_missing:
                    st.markdown(f"🔴 {n}")
        else:
            st.info("No students registered yet, or Google Sheet not connected.")

    # ── Tab 3: Leaderboard control ──
    with admin_tab3:
        st.markdown("### 🏆 Leaderboard Overview")
        users_df = load_sheet("Users")
        if not users_df.empty and "Name" in users_df.columns:
            lb = users_df[["Name","XP","Streak"]].copy() if "XP" in users_df.columns else users_df[["Name"]].copy()
            if "XP" in lb.columns:
                lb = lb.sort_values("XP", ascending=False)
            st.dataframe(lb, use_container_width=True)
        else:
            st.info("Connect Google Sheet to see live leaderboard.")

        st.markdown("---")
        st.markdown("### 📢 Send WhatsApp Message Template")
        if st.button("Generate Message", key="gen_wa"):
            top = "Sara" # Would be dynamic from DB
            msg = f"🇩🇪 يا جماعة، الليلة {top} كانت الأولى وخلصت كل مهامها! 🏆 مين رح يلحق عليها بكرة؟ يلا بكرة محدش يعمل excuse 💪 #German_Mastery_Camp"
            st.code(msg)
            st.caption("Copy this and send it to your WhatsApp group!")

    # ── Tab 4: Submissions ──
    with admin_tab4:
        st.markdown("### 📝 Student Writing Submissions")
        sub_df = load_sheet("Submissions")
        if not sub_df.empty:
            st.dataframe(sub_df, use_container_width=True)
        else:
            st.info("No writing submissions yet.")


# ════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:10px 0 16px;'>
            <div style='font-size:2.2rem;'>🇩🇪</div>
            <div style='font-family:"Playfair Display",serif;font-size:1.2rem;color:#f5c518;font-weight:700;'>German Mastery Camp</div>
            <div style='color:#555;font-size:.78rem;margin-top:2px;'>90-Day Intensive</div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.logged_in and st.session_state.user:
            name = st.session_state.user.get("Name","Learner")
            admin_tag = ' <span style="background:#f5c518;color:#000;border-radius:4px;padding:1px 6px;font-size:.65rem;font-weight:700;">ADMIN</span>' if is_admin() else ""
            st.markdown(f"""
            <div style='text-align:center;margin-bottom:12px;'>
                <div style='font-size:1.8rem;'>{"⚙️" if is_admin() else "👤"}</div>
                <div style='font-weight:600;font-size:.95rem;'>{name}{admin_tag}</div>
                <div style='color:#555;font-size:.75rem;'>⭐ {user_xp()} XP</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        pages = {
            "🏠 Home":          "home",
            "🗺️ Roadmap":       "roadmap",
            "📅 Daily Mission": "daily",
            "🤖 AI Copilot":    "ai",
            "🎮 Games":         "games",
            "🏆 Leaderboard":   "leaderboard",
            "🔬 Phonetics Lab": "phonetics",
            "📚 Resources":     "resources",
        }
        if is_admin():
            pages["⚙️ Admin Panel"] = "admin"

        for label, key in pages.items():
            active = st.session_state.current_page == key
            style = "color:#f5c518!important;" if active else ""
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        # Mini progress
        done = len(st.session_state.completed_days)
        st.markdown(f"**Progress: {done}/90 days**")
        st.progress(done / 90)
        streak = compute_streak(st.session_state.completed_days)
        st.markdown(f"<div style='display:flex;justify-content:space-between;color:#888;font-size:.82rem;'><span>🔥 {streak} day streak</span><span>⭐ {user_xp()} XP</span></div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Sign Out", key="signout"):
            save_progress()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_auth()
else:
    render_sidebar()
    page = st.session_state.current_page
    if   page == "home":       page_home()
    elif page == "roadmap":    page_roadmap()
    elif page == "daily":      page_daily()
    elif page == "ai":         page_ai_copilot()
    elif page == "games":      page_games()
    elif page == "leaderboard":page_leaderboard()
    elif page == "phonetics":  page_phonetics()
    elif page == "resources":  page_resources()
    elif page == "admin":
        if is_admin():         page_admin()
        else:                  st.error("🔒 Admin access required.")
    else:
        page_home()

    # Footer
    st.markdown("---")
    st.markdown("""<div style='text-align:center;color:#333;font-size:.78rem;padding:8px 0 18px;'>
        🇩🇪 German Mastery Camp &nbsp;|&nbsp; <em>Viel Erfolg!</em>
    </div>""", unsafe_allow_html=True)
