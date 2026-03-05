# ═══════════════════════════════════════════════════════════════════════════
#  GERMAN MASTERY CAMP  v4.0  —  High-End Edition
#  Glassmorphism UI · Groq AI · gTTS Audio · Visual Learning · Plotly Dashboard
# ═══════════════════════════════════════════════════════════════════════════

# ── 1. FORCE INSTALL ─────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    try:
        subprocess.check_call([sys.executable,"-m","pip","install",pkg,"-q"],
                              stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except Exception: pass

for _pkg in ["groq","bcrypt","gtts","plotly","gspread","google-auth"]:
    _install(_pkg)

# ── 2. IMPORTS ────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import json, random, datetime, time, io, base64, re, hashlib, math

try:
    import bcrypt as _bcrypt; BCRYPT_OK = True
except ImportError: BCRYPT_OK = False

try:
    from gtts import gTTS; GTTS_OK = True
except ImportError: GTTS_OK = False

try:
    from groq import Groq; GROQ_OK = True
except ImportError: GROQ_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px; PLOTLY_OK = True
except ImportError: PLOTLY_OK = False

try:
    import gspread
    from google.oauth2.service_account import Credentials; GSHEETS_OK = True
except ImportError: GSHEETS_OK = False

# ── 3. PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇩🇪 German Mastery Camp",
    page_icon="🇩🇪", layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
#  GLASSMORPHISM CSS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,400&display=swap');

:root{
  --red:#cc0000; --gold:#f5c518; --gold2:#d4a017;
  --bg:#060810; --glass:rgba(255,255,255,0.04);
  --glass2:rgba(255,255,255,0.08); --border:rgba(255,255,255,0.10);
  --border2:rgba(245,197,24,0.30); --text:#f0eee8; --muted:#8a8a9a;
  --success:#22c55e; --info:#60a5fa; --blur:blur(15px);
  --shadow:0 8px 32px rgba(0,0,0,0.5);
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:var(--bg)!important;color:var(--text)!important;}
.stApp{
  background:
    radial-gradient(ellipse 80% 50% at 20% -10%,rgba(204,0,0,.12) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 110%,rgba(245,197,24,.08) 0%,transparent 55%),
    linear-gradient(160deg,#060810 0%,#0e0c18 40%,#100808 100%);
  background-attachment:fixed;
}
h1,h2,h3{font-family:'Playfair Display',serif!important;}
h1{background:linear-gradient(135deg,var(--gold),#fff 60%,var(--gold));
   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
   font-size:2.4rem!important;font-weight:900!important;}
h2{color:var(--red)!important;} h3{color:var(--gold2)!important;}

[data-testid="stSidebar"]{background:rgba(6,8,16,.95)!important;backdrop-filter:var(--blur)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
[data-testid="stSidebar"] .stButton>button{background:var(--glass)!important;border:1px solid var(--border)!important;color:var(--text)!important;font-size:.88rem!important;text-align:left!important;padding:10px 16px!important;border-radius:10px!important;margin-bottom:4px!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(204,0,0,.15)!important;border-color:var(--red)!important;}

.g-card{background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:20px;padding:24px 28px;margin-bottom:16px;box-shadow:var(--shadow);transition:border-color .2s,transform .2s;}
.g-card:hover{border-color:rgba(245,197,24,.2);transform:translateY(-2px);}
.g-card.gold{border-color:var(--border2);}
.g-card.red{border-color:rgba(204,0,0,.4);}
.g-card.green{border-color:rgba(34,197,94,.3);}

[data-testid="stMetric"]{background:var(--glass)!important;backdrop-filter:var(--blur)!important;border:1px solid var(--border)!important;border-radius:16px!important;padding:18px!important;}
[data-testid="stMetricValue"]{color:var(--gold)!important;font-size:1.9rem!important;font-weight:700!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.8rem!important;}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,var(--red),var(--gold))!important;border-radius:99px!important;}

.stButton>button{background:linear-gradient(135deg,rgba(204,0,0,.8),rgba(139,0,0,.9))!important;color:#fff!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:10px!important;font-weight:600!important;backdrop-filter:var(--blur)!important;transition:all .18s ease!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(204,0,0,.4)!important;}
.gold-btn .stButton>button{background:linear-gradient(135deg,var(--gold),var(--gold2))!important;color:#000!important;border-color:transparent!important;}
.gold-btn .stButton>button:hover{box-shadow:0 8px 24px rgba(245,197,24,.35)!important;}
.green-btn .stButton>button{background:linear-gradient(135deg,#16a34a,#166534)!important;color:#fff!important;}
.ghost-btn .stButton>button{background:var(--glass)!important;border-color:var(--border)!important;color:var(--muted)!important;}

[data-testid="stTabs"] button{color:var(--muted)!important;font-weight:500!important;border-radius:8px 8px 0 0!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--gold)!important;border-bottom:2px solid var(--gold)!important;background:rgba(245,197,24,.05)!important;}

[data-testid="stTextInput"]>div>div,[data-testid="stTextArea"]>div>div,[data-testid="stSelectbox"]>div{background:var(--glass)!important;backdrop-filter:var(--blur)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;}

.hero{background:radial-gradient(ellipse 120% 100% at 50% 0%,rgba(204,0,0,.15) 0%,transparent 65%),var(--glass);backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:24px;padding:48px 40px;text-align:center;margin-bottom:28px;position:relative;overflow:hidden;animation:heroFade .6s ease;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;background:linear-gradient(135deg,var(--gold),#fff 50%,var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.15;margin-bottom:8px;}
.hero-sub{color:var(--muted);font-size:1.05rem;margin-bottom:20px;line-height:1.6;}
.hero-pills{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:16px;}
.pill{background:rgba(255,255,255,.06);border:1px solid var(--border);border-radius:99px;padding:5px 16px;font-size:.82rem;color:var(--muted);}
.pill.active{border-color:var(--border2);color:var(--gold);}

.mantra-box{background:linear-gradient(135deg,rgba(245,197,24,.05),rgba(204,0,0,.05));border:1px solid var(--border2);border-radius:16px;padding:22px 28px;text-align:center;font-style:italic;color:var(--gold);font-size:1.05rem;font-family:'Playfair Display',serif;margin-bottom:22px;backdrop-filter:var(--blur);}

.dict-card{background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:18px;padding:20px 22px;margin-bottom:12px;transition:border-color .2s;position:relative;overflow:hidden;}
.dict-card:hover{border-color:var(--border2);}
.dict-card::before{content:'';position:absolute;left:0;top:0;width:3px;height:100%;background:linear-gradient(180deg,var(--red),var(--gold));}
.dict-word{font-family:'Playfair Display',serif;font-size:1.9rem;color:var(--gold);font-weight:700;}
.dict-ipa{color:var(--muted);font-size:.82rem;font-style:italic;margin-top:1px;}
.dict-badge{display:inline-block;background:rgba(245,197,24,.1);border:1px solid var(--border2);border-radius:6px;padding:1px 8px;font-size:.7rem;color:var(--gold);margin-left:8px;vertical-align:middle;}
.dict-translations{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0;}
.trans-ar{background:rgba(204,0,0,.1);border:1px solid rgba(204,0,0,.25);border-radius:8px;padding:4px 12px;font-size:.9rem;color:#ffb3b3;direction:rtl;}
.trans-en{background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.25);border-radius:8px;padding:4px 12px;font-size:.9rem;color:#86efac;}
.dict-example{background:rgba(0,0,0,.25);border-radius:10px;padding:12px 14px;margin:10px 0;}
.ex-de{font-size:.98rem;color:var(--text);font-weight:500;line-height:1.7;}
.ex-ar{font-size:.85rem;color:var(--muted);direction:rtl;margin-top:4px;}
.ex-en{font-size:.83rem;color:var(--muted);font-style:italic;}
.input-box{background:rgba(96,165,250,.05);border:1px solid rgba(96,165,250,.2);border-radius:10px;padding:12px;margin-top:8px;}
.output-box{background:rgba(34,197,94,.04);border:1px solid rgba(34,197,94,.2);border-radius:10px;padding:12px;margin-top:8px;}

.play-btn{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,rgba(96,165,250,.6),rgba(37,99,235,.7));border:none;border-radius:20px;padding:5px 14px;font-size:.78rem;font-weight:600;color:#fff;cursor:pointer;transition:all .15s;margin-top:6px;}
.play-btn:hover{transform:scale(1.04);box-shadow:0 4px 14px rgba(96,165,250,.35);}

.day-node{display:flex;align-items:center;gap:14px;background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin-bottom:8px;transition:all .2s;}
.day-node.done{border-left:3px solid var(--success);}
.day-node.current{border-left:3px solid var(--gold);background:rgba(245,197,24,.04);}
.day-node.locked{opacity:.35;pointer-events:none;}
.node-num{background:linear-gradient(135deg,var(--red),#8b0000);color:#fff;border-radius:50%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0;}
.node-num.done{background:linear-gradient(135deg,#16a34a,#166534);}
.node-num.locked{background:#222;}

.lb-row{display:flex;align-items:center;background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:12px;padding:12px 18px;margin-bottom:8px;gap:12px;}
.lb-rank{font-size:1.3rem;width:32px;} .lb-name{flex:1;font-weight:600;} .lb-xp{color:var(--gold);font-weight:700;}

.game-card{background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:20px;padding:30px;text-align:center;cursor:pointer;transition:all .2s;}
.game-card:hover{border-color:var(--border2);transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.4);}

.quiz-option{background:var(--glass);border:1px solid var(--border);border-radius:12px;padding:14px 18px;margin-bottom:8px;cursor:pointer;transition:all .15s;}
.quiz-option:hover{border-color:var(--border2);background:rgba(245,197,24,.05);}
.quiz-option.correct{border-color:var(--success)!important;background:rgba(34,197,94,.08)!important;}
.quiz-option.wrong{border-color:#ef4444!important;background:rgba(239,68,68,.08)!important;}

.hist-chip{display:inline-block;background:var(--glass);border:1px solid var(--border);border-radius:99px;padding:3px 12px;font-size:.78rem;color:var(--muted);margin:3px;cursor:pointer;}
.hist-chip:hover{border-color:var(--border2);color:var(--gold);}
.flag-bar{height:4px;background:linear-gradient(90deg,#1a1a1a 33%,var(--red) 33% 66%,var(--gold) 66%);border-radius:99px;margin-bottom:24px;}
.admin-badge{display:inline-block;background:var(--gold);color:#000;border-radius:6px;padding:2px 10px;font-size:.72rem;font-weight:700;}

@keyframes heroFade{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}} .fade-in{animation:fadeIn .4s ease;}
::-webkit-scrollbar{width:6px;} ::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:3px;}
div[data-testid="column"]{padding:6px!important;}
@media(max-width:768px){.hero-title{font-size:1.8rem;}.dict-word{font-size:1.4rem;}h1{font-size:1.7rem!important;}.hero{padding:28px 18px;}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  SECRETS & CONFIG
# ═══════════════════════════════════════════════════════════════════════════
def _s(k,fb=""): 
    try: return st.secrets[k]
    except: return fb

GROQ_MODEL = "llama-3.3-70b-versatile"

def groq_client():
    k=_s("GROQ_API_KEY")
    if not k or not GROQ_OK: return None
    try: return Groq(api_key=k)
    except: return None

def has_groq(): return bool(_s("GROQ_API_KEY")) and GROQ_OK

# ═══════════════════════════════════════════════════════════════════════════
#  GOOGLE SHEETS
# ═══════════════════════════════════════════════════════════════════════════
SCOPES=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

@st.cache_resource(ttl=60)
def get_gc():
    if not GSHEETS_OK: return None
    try:
        creds=Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]),scopes=SCOPES)
        return gspread.authorize(creds)
    except: return None

@st.cache_data(ttl=30)
def load_sheet(tab):
    gc=get_gc()
    if not gc: return pd.DataFrame()
    try:
        wk=gc.open_by_key(_s("sheet_id")).worksheet(tab)
        return pd.DataFrame(wk.get_all_records())
    except: return pd.DataFrame()

def write_row(tab,row):
    gc=get_gc()
    if not gc: return False
    try:
        gc.open_by_key(_s("sheet_id")).worksheet(tab).append_row(row,value_input_option="USER_ENTERED")
        load_sheet.clear(); return True
    except: return False

def save_progress():
    if not st.session_state.user: return
    gc=get_gc()
    if not gc: return
    try:
        wk=gc.open_by_key(_s("sheet_id")).worksheet("Users")
        records=wk.get_all_records(); headers=wk.row_values(1)
        email=st.session_state.user["Email"]
        days_json=json.dumps(sorted(st.session_state.completed_days))
        xp=st.session_state.xp; streak=_streak(st.session_state.completed_days)
        for i,r in enumerate(records,2):
            if str(r.get("Email","")).lower()==email.lower():
                for col,val in [("XP",xp),("Streak",streak),("CompletedDays",days_json)]:
                    if col in headers: wk.update_cell(i,headers.index(col)+1,val)
                break
        load_sheet.clear()
    except: pass

# ═══════════════════════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════════════════════
def _hash(pw):
    if BCRYPT_OK: return _bcrypt.hashpw(pw.encode(),_bcrypt.gensalt()).decode()
    return hashlib.sha256(pw.encode()).hexdigest()

def _verify(pw,hashed):
    try:
        if BCRYPT_OK and str(hashed).startswith("$2"): return _bcrypt.checkpw(pw.encode(),str(hashed).encode())
        return hashlib.sha256(pw.encode()).hexdigest()==hashed
    except: return False

def get_user(email):
    df=load_sheet("Users")
    if df.empty or "Email" not in df.columns: return None
    r=df[df["Email"].str.lower()==email.lower()]
    return r.iloc[0].to_dict() if not r.empty else None

def register_user(name,email,pw):
    if get_user(email): return False
    return write_row("Users",[name,email,_hash(pw),0,0,1,"[]",datetime.datetime.now().isoformat(),""])

def login_user(email,pw):
    u=get_user(email)
    return u if (u and _verify(pw,str(u.get("Password","")))) else None

# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def _streak(done):
    if not done: return 0
    s,d=0,max(done)
    while d in done: s+=1; d-=1
    return s

def _phase(day):
    if day<=30: return "Foundation"
    if day<=60: return "Construction"
    return "Activation"

def _unlocked(day): return day==1 or (day-1) in st.session_state.completed_days

def _get_level(xp):
    levels=[(0,"Anfänger"),(100,"Lernender"),(300,"Entdecker"),(600,"Schüler"),
            (1000,"Fortgeschritten"),(1500,"Kenner"),(2500,"Experte"),(4000,"Meister"),(6000,"Großmeister")]
    name="Anfänger"
    for t,n in levels:
        if xp>=t: name=n
    return name

# ═══════════════════════════════════════════════════════════════════════════
#  AUDIO  (gTTS + fallback to Google TTS URL)
# ═══════════════════════════════════════════════════════════════════════════
import urllib.parse

@st.cache_data(ttl=3600)
def tts_b64(text,lang="de"):
    if not GTTS_OK: return None
    try:
        buf=io.BytesIO()
        gTTS(text=text,lang=lang,slow=False).write_to_fp(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    except: return None

def autoplay_html(b64):
    return f'<audio autoplay style="display:none"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

def play_btn_html(text_de, label="🔊 Listen"):
    b64=tts_b64(text_de)
    if not b64:
        url=f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(text_de[:100])}&tl=de"
        return f'<a href="{url}" target="_blank" class="play-btn">{label}</a>'
    aid=f"a{hashlib.md5(text_de.encode()).hexdigest()[:8]}"
    return (f'<audio id="{aid}" src="data:audio/mp3;base64,{b64}"></audio>'
            f'<button class="play-btn" onclick="document.getElementById(\'{aid}\').play()">{label}</button>')

# ═══════════════════════════════════════════════════════════════════════════
#  GROQ AI
# ═══════════════════════════════════════════════════════════════════════════
def groq_chat(system,messages,user_msg,max_tokens=700):
    cl=groq_client()
    if not cl: return "⚠️ Add GROQ_API_KEY to secrets.toml"
    try:
        hist=[{"role":m["role"],"content":m["content"]} for m in messages[-12:]]
        hist.append({"role":"user","content":user_msg})
        resp=cl.chat.completions.create(
            model=GROQ_MODEL,max_tokens=max_tokens,temperature=0.7,
            messages=[{"role":"system","content":system}]+hist,
        )
        return resp.choices[0].message.content
    except Exception as e: return f"AI error: {e}"

def groq_correct(text):
    return groq_chat(
        "You are Klaus, an expert German tutor. Correct the student's German.\n"
        "1. Write CORRECTED version in **bold**\n"
        "2. List each error with explanation (Arabic+English)\n"
        "3. Give the grammar rule\n4. End with one encouraging German sentence.",
        [],f"Correct my German:\n{text}",800
    )

def groq_quiz(level,vocab):
    words=", ".join([f"{w['word']} ({w['en']})" for w in vocab[:8]])
    raw=groq_chat(
        "You are a German quiz generator. Return ONLY valid JSON, no markdown.\n"
        '{"question":"...","options":["A","B","C","D"],"answer":"A","explanation":"...","german_example":"..."}',
        [],f"Level:{level} Words:{words} — Create ONE multiple choice question.",400
    )
    try:
        raw=raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(raw)
    except:
        return {"question":"What does 'lernen' mean?","options":["To eat","To learn","To sleep","To run"],
                "answer":"To learn","explanation":"'Lernen' = to learn","german_example":"Ich lerne Deutsch."}

# ═══════════════════════════════════════════════════════════════════════════
#  VOCABULARY (import from config.py or use inline fallback)
# ═══════════════════════════════════════════════════════════════════════════
try:
    from config import (DICTIONARY,search_dictionary,get_dict_by_level,get_random_words,
                        get_all_categories,MANTRAS,PHASES,PHASE_MAP,CULTURAL_DROPS,
                        RESOURCES,PHONETICS,MINIMAL_PAIRS,GRAMMAR_TOPICS,BADGES,XP_RULES)
    CONFIG_OK=True
except ImportError:
    CONFIG_OK=False
    DICTIONARY=[
        {"word":"Haus","gender":"das","plural":"Häuser","level":"A1","category":"🏠 Zuhause","ar":"بيت","en":"house","ipa":"[haʊs]","example_de":"Das Haus ist groß.","example_ar":"البيت كبير.","example_en":"The house is big.","input_image_keyword":"house Germany","output_prompt_ar":"صف البيت."},
        {"word":"Wasser","gender":"das","plural":"-","level":"A1","category":"🍽️ Essen","ar":"ماء","en":"water","ipa":"[ˈvasɐ]","example_de":"Ich trinke Wasser.","example_ar":"أشرب ماءً.","example_en":"I drink water.","input_image_keyword":"glass water","output_prompt_ar":"اكتب عما تشربه."},
        {"word":"lernen","gender":None,"plural":None,"level":"A1","category":"🔧 Verben","ar":"يتعلم","en":"to learn","ipa":"[ˈlɛʁnən]","example_de":"Ich lerne Deutsch.","example_ar":"أتعلم الألمانية.","example_en":"I learn German.","input_image_keyword":"student studying","output_prompt_ar":"ماذا تتعلم؟"},
        {"word":"Familie","gender":"die","plural":"Familien","level":"A1","category":"👨‍👩‍👧 Familie","ar":"عائلة","en":"family","ipa":"[faˈmiːliə]","example_de":"Meine Familie ist groß.","example_ar":"عائلتي كبيرة.","example_en":"My family is big.","input_image_keyword":"family portrait","output_prompt_ar":"صف عائلتك."},
        {"word":"Zeit","gender":"die","plural":"Zeiten","level":"A1","category":"⏰ Zeit","ar":"وقت","en":"time","ipa":"[tsaɪt]","example_de":"Ich habe keine Zeit.","example_ar":"ليس لدي وقت.","example_en":"I have no time.","input_image_keyword":"clock watch","output_prompt_ar":"كم ساعة تدرس؟"},
        {"word":"Arbeit","gender":"die","plural":"Arbeiten","level":"A1","category":"💼 Beruf","ar":"عمل","en":"work","ipa":"[ˈaʁbaɪt]","example_de":"Die Arbeit beginnt um neun.","example_ar":"يبدأ العمل الساعة التاسعة.","example_en":"Work starts at nine.","input_image_keyword":"office work laptop","output_prompt_ar":"صف عملك."},
        {"word":"Sprache","gender":"die","plural":"Sprachen","level":"A1","category":"📚 Bildung","ar":"لغة","en":"language","ipa":"[ˈʃpʁaːxə]","example_de":"Deutsch ist eine schöne Sprache.","example_ar":"الألمانية لغة جميلة.","example_en":"German is beautiful.","input_image_keyword":"language flags world","output_prompt_ar":"لماذا تتعلم الألمانية؟"},
        {"word":"gut","gender":None,"plural":None,"level":"A1","category":"📐 Adjektive","ar":"جيد","en":"good","ipa":"[ɡuːt]","example_de":"Das ist sehr gut!","example_ar":"هذا جيد جداً!","example_en":"That is very good!","input_image_keyword":"thumbs up good","output_prompt_ar":"ما الذي يجعلك تقول 'sehr gut' اليوم؟"},
        {"word":"schön","gender":None,"plural":None,"level":"A1","category":"📐 Adjektive","ar":"جميل","en":"beautiful","ipa":"[ʃøːn]","example_de":"Das Wetter ist schön.","example_ar":"الطقس جميل.","example_en":"The weather is beautiful.","input_image_keyword":"beautiful landscape Germany","output_prompt_ar":"صف شيئاً جميلاً تراه."},
        {"word":"können","gender":None,"plural":None,"level":"A1","category":"🔧 Verben","ar":"يستطيع","en":"can","ipa":"[ˈkœnən]","example_de":"Ich kann Deutsch sprechen.","example_ar":"أستطيع التحدث بالألمانية.","example_en":"I can speak German.","input_image_keyword":"ability skill superhero","output_prompt_ar":"ماذا تستطيع فعله بالألمانية الآن؟"},
    ]
    def search_dictionary(q):
        q=q.lower()
        return [w for w in DICTIONARY if q in w["word"].lower() or q in w["en"].lower() or q in w["ar"]]
    def get_dict_by_level(lv): return [w for w in DICTIONARY if w["level"]==lv]
    def get_random_words(n=10,level=None):
        pool=get_dict_by_level(level) if level else DICTIONARY
        return random.sample(pool,min(n,len(pool)))
    def get_all_categories():
        seen,cats=set(),[]
        for w in DICTIONARY:
            if w["category"] not in seen: seen.add(w["category"]); cats.append(w["category"])
        return cats
    MANTRAS=[('"Übung macht den Meister."',"Practice makes perfect.")]
    PHASES=[
        {"name":"Foundation","emoji":"🏗️","days":list(range(1,31)),"goal":"Master basics.","cefr":"Pre-A1→A1","color":"#f5c518"},
        {"name":"Construction","emoji":"🧱","days":list(range(31,61)),"goal":"Build sentences.","cefr":"A1→A2","color":"#cc0000"},
        {"name":"Activation","emoji":"⚡","days":list(range(61,91)),"goal":"Real contexts.","cefr":"A2→B1","color":"#22c55e"},
    ]
    PHASE_MAP={}
    for _ph in PHASES:
        for _d in _ph["days"]: PHASE_MAP[_d]=_ph["name"]
    CULTURAL_DROPS=[{"week":1,"title":"Pünktlichkeit 🕐","body":"Punctuality is a form of respect in Germany. 5 min early = respectful."}]
    RESOURCES=[]
    PHONETICS=[
        {"sym":"r","name":"Das R","ipa":"[ʁ]","desc":"Guttural — gargle softly","yt":"oRpSJXMJUDg","example_words":["rot","reisen"]},
        {"sym":"ch","name":"Das CH","ipa":"[ç]/[x]","desc":"ich-Laut vs ach-Laut","yt":"pN3Aqs9BGLM","example_words":["ich","acht"]},
        {"sym":"ä","name":"Das Ä","ipa":"[ɛ]","desc":"Like 'air' but shorter","yt":"XbiBS5YIQB0","example_words":["Käse","Mädchen"]},
        {"sym":"ö","name":"Das Ö","ipa":"[ø]","desc":"Round lips, say 'e'","yt":"XbiBS5YIQB0","example_words":["schön","hören"]},
        {"sym":"ü","name":"Das Ü","ipa":"[y]","desc":"Round lips, say 'i'","yt":"XbiBS5YIQB0","example_words":["über","grün"]},
        {"sym":"ß","name":"Das ß","ipa":"[sː]","desc":"Sharp SS","yt":"oRpSJXMJUDg","example_words":["Straße","heiß"]},
    ]
    MINIMAL_PAIRS=[("bitten","bieten","to ask / to offer"),("Hölle","Höhle","hell / cave"),("Bach","Buch","stream / book"),("lesen","essen","to read / to eat")]
    GRAMMAR_TOPICS={"Foundation":[],"Construction":[],"Activation":[]}
    BADGES=[]
    XP_RULES={"complete_day":20,"flashcard_correct":3,"word_match":15,"sentence_scramble":20,"save_word":2,"grammar_exercise":5}

# ═══════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════
_D={"logged_in":False,"user":None,"is_admin":False,"page":"home",
    "completed_days":set(),"xp":0,"daily_tasks":{},"ai_messages":[],
    "game_state":{},"search_history":[],"quiz_state":None,
    "games_played":0,"games_won":0,"submissions_count":0,"saved_words":[]}
for k,v in _D.items():
    if k not in st.session_state: st.session_state[k]=v

def sync_from_db():
    if st.session_state.user:
        try: st.session_state.completed_days=set(json.loads(str(st.session_state.user.get("CompletedDays","[]"))))
        except: pass
        try: st.session_state.xp=int(st.session_state.user.get("XP",0))
        except: pass

# ═══════════════════════════════════════════════════════════════════════════
#  VISUAL LEARNING — Image grid (Unsplash source)
# ═══════════════════════════════════════════════════════════════════════════
def unsplash(kw,w=400,h=240):
    k=kw.replace(" ",",")
    return f"https://source.unsplash.com/{w}x{h}/?{k}"

def image_grid_html(entries):
    html='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px;margin:12px 0;">'
    for e in entries:
        img=unsplash(e.get("input_image_keyword",e["word"]))
        html+=f"""<div style="background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);
                   border-radius:14px;overflow:hidden;transition:transform .2s;"
                  onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
          <img src="{img}" style="width:100%;height:120px;object-fit:cover;" loading="lazy" onerror="this.style.display='none'">
          <div style="padding:10px 12px;">
            <div style="font-size:1rem;font-weight:700;color:var(--gold);font-family:'Playfair Display',serif;">{e['word']}</div>
            <div style="font-size:.8rem;color:var(--muted);direction:rtl;">{e['ar']}</div>
          </div></div>"""
    return html+"</div>"

# ═══════════════════════════════════════════════════════════════════════════
#  PLOTLY CHARTS
# ═══════════════════════════════════════════════════════════════════════════
def chart_gauge(done,total=90):
    if not PLOTLY_OK: return None
    fig=go.Figure(go.Indicator(
        mode="gauge+number",value=done,
        title={"text":"Days Done","font":{"color":"#aaa","size":13}},
        gauge={"axis":{"range":[0,total],"tickcolor":"#444","tickfont":{"color":"#666"}},
               "bar":{"color":"rgba(245,197,24,.75)","thickness":.3},
               "bgcolor":"rgba(0,0,0,0)","borderwidth":0,
               "steps":[{"range":[0,30],"color":"rgba(204,0,0,.12)"},
                         {"range":[30,60],"color":"rgba(245,197,24,.08)"},
                         {"range":[60,90],"color":"rgba(34,197,94,.1)"}]},
        number={"suffix":f"/{total}","font":{"color":"#f5c518","size":26}},
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      font={"color":"#f8f5ef"},margin=dict(l=20,r=20,t=40,b=10),height=220)
    return fig

def chart_xp(done):
    if not PLOTLY_OK or not done: return None
    ds=sorted(done); xp=[i*20 for i in range(1,len(ds)+1)]
    fig=go.Figure(go.Scatter(x=list(range(1,len(ds)+1)),y=xp,mode="lines+markers",
        line={"color":"#f5c518","width":2},marker={"color":"#cc0000","size":5},
        fill="tozeroy",fillcolor="rgba(245,197,24,.06)"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font={"color":"#f8f5ef"},height=200,margin=dict(l=10,r=10,t=30,b=20),
        xaxis={"title":"Sessions","gridcolor":"rgba(255,255,255,.05)","tickfont":{"size":9}},
        yaxis={"title":"XP","gridcolor":"rgba(255,255,255,.05)","tickfont":{"size":9}},
        title={"text":"XP Growth","font":{"color":"#f5c518","size":12}},showlegend=False)
    return fig

def chart_radar(done):
    if not PLOTLY_OK: return None
    f=len([d for d in done if 1<=d<=30])/30
    c=len([d for d in done if 31<=d<=60])/30
    a=len([d for d in done if 61<=d<=90])/30
    fig=go.Figure(go.Scatterpolar(r=[f*100,c*100,a*100,f*100],
        theta=["Foundation","Construction","Activation","Foundation"],
        fill="toself",fillcolor="rgba(204,0,0,.12)",line={"color":"#f5c518","width":2}))
    fig.update_layout(polar={"bgcolor":"rgba(0,0,0,0)",
        "radialaxis":{"visible":True,"range":[0,100],"tickfont":{"color":"#444"},"gridcolor":"rgba(255,255,255,.07)"},
        "angularaxis":{"tickfont":{"color":"#999"},"gridcolor":"rgba(255,255,255,.07)"}},
        paper_bgcolor="rgba(0,0,0,0)",font={"color":"#f8f5ef"},height=220,margin=dict(l=20,r=20,t=30,b=10),showlegend=False)
    return fig

def chart_heatmap(done):
    if not PLOTLY_OK: return None
    z=[[1 if (r*10+c+1) in done else 0 for c in range(10)] for r in range(9)]
    fig=go.Figure(go.Heatmap(z=z,colorscale=[[0,"rgba(255,255,255,.04)"],[1,"rgba(245,197,24,.8)"]],showscale=False,xgap=3,ygap=3))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font={"color":"#f8f5ef"},height=200,margin=dict(l=10,r=10,t=35,b=10),
        title={"text":"90-Day Calendar","font":{"color":"#f5c518","size":12}},
        xaxis={"visible":False},yaxis={"visible":False})
    return fig

# ═══════════════════════════════════════════════════════════════════════════
#  WORD CARD RENDERER
# ═══════════════════════════════════════════════════════════════════════════
def render_word_card(e,show_output=True):
    g=f"{e['gender']} " if e.get("gender") and e["gender"] not in ["—","None",None] else ""
    pl=f" · Pl: {e['plural']}" if e.get("plural") and str(e.get("plural")) not in ["-","None","—",""] else ""
    aud=play_btn_html(e["word"])
    ex_aud=play_btn_html(e["example_de"],"🔊 Example")
    st.markdown(f"""<div class="dict-card fade-in">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
        <div>
          <span class="dict-word">{g}{e['word']}</span>
          <span class="dict-badge">{e.get('level','')}</span>
          <div class="dict-ipa">{e.get('ipa','')} &nbsp;·&nbsp; {e.get('category','')}{pl}</div>
        </div>
        <div>{aud}</div>
      </div>
      <div class="dict-translations">
        <span class="trans-ar">🇪🇬 {e['ar']}</span>
        <span class="trans-en">🇬🇧 {e['en']}</span>
      </div>
      <div class="dict-example">
        <div class="ex-de">💬 {e['example_de']}</div>
        {ex_aud}
        <div class="ex-ar">↳ {e['example_ar']}</div>
        <div class="ex-en">↳ {e['example_en']}</div>
      </div>
    </div>""",unsafe_allow_html=True)
    if show_output and e.get("input_image_keyword"):
        img=unsplash(e["input_image_keyword"])
        st.markdown(f"""<div class="input-box">
          <div style="font-size:.72rem;color:var(--info);text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">📥 Comprehensible Input</div>
          <img src="{img}" style="width:100%;max-height:170px;object-fit:cover;border-radius:8px;margin-bottom:6px;"
               loading="lazy" onerror="this.parentElement.style.display='none'">
          <div style="font-size:.78rem;color:var(--muted);">🔍 {e['input_image_keyword']}</div>
        </div>
        <div class="output-box">
          <div style="font-size:.72rem;color:var(--success);text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">📤 Output Practice</div>
          <div style="font-size:.86rem;color:var(--muted);direction:rtl;">✏️ {e.get('output_prompt_ar','')}</div>
        </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: AUTH
# ═══════════════════════════════════════════════════════════════════════════
def page_auth():
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    _,mid,_=st.columns([1,2,1])
    with mid:
        st.markdown("""<div class="g-card" style="text-align:center;padding:40px 32px;">
          <div style="font-size:3.5rem;">🇩🇪</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.7rem;background:linear-gradient(135deg,#f5c518,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;margin:6px 0;">German Mastery Camp</div>
          <div style="color:var(--muted);font-size:.85rem;">Your 90-day journey to German fluency</div>
        </div>""",unsafe_allow_html=True)
        ti,tu=st.tabs(["🔑 Sign In","🆕 Register"])
        with ti:
            email=st.text_input("Email",key="li_e",placeholder="your@email.com")
            pw=st.text_input("Password",type="password",key="li_p",placeholder="••••••••")
            c1,c2=st.columns(2)
            with c1:
                if st.button("Sign In →",use_container_width=True,key="btn_li"):
                    if not email or not pw: st.error("Fill all fields.")
                    elif get_gc() is None:
                        st.session_state.update({"logged_in":True,"user":{"Name":email.split("@")[0].title(),"Email":email,"XP":0,"Streak":0,"CompletedDays":"[]"}})
                        st.rerun()
                    else:
                        u=login_user(email,pw)
                        if u: st.session_state.update({"logged_in":True,"user":u}); sync_from_db(); st.rerun()
                        else: st.error("Invalid credentials.")
            with c2:
                adm=st.text_input("Admin password",type="password",key="adm_i",placeholder="Admin only")
                if st.button("Admin →",key="btn_adm"):
                    if adm==_s("admin_password","admin1234"):
                        st.session_state.update({"logged_in":True,"is_admin":True,"user":{"Name":"Admin","Email":"admin@camp.de","XP":9999,"Streak":90,"CompletedDays":"[]"}})
                        st.rerun()
                    else: st.error("Wrong admin password.")
        with tu:
            n=st.text_input("Full Name",key="ru_n",placeholder="Ahmed Mohamed")
            e2=st.text_input("Email",key="ru_e",placeholder="your@email.com")
            p2=st.text_input("Password (min 6)",type="password",key="ru_p")
            p2c=st.text_input("Confirm Password",type="password",key="ru_pc")
            if st.button("Create Account →",use_container_width=True,key="btn_ru"):
                if not all([n,e2,p2,p2c]): st.error("Fill all fields.")
                elif p2!=p2c: st.error("Passwords don't match.")
                elif len(p2)<6: st.error("Min 6 characters.")
                elif get_gc() is None:
                    st.session_state.update({"logged_in":True,"user":{"Name":n,"Email":e2,"XP":0,"Streak":0,"CompletedDays":"[]"}})
                    st.success("Welcome! (Demo mode)"); time.sleep(1); st.rerun()
                elif register_user(n,e2,p2): st.success("Account created! Sign in now.")
                else: st.error("Email already registered.")
        st.markdown('<div style="text-align:center;color:#444;font-size:.75rem;margin-top:10px;">Open registration · Free forever 🎉</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════
def page_home():
    name=st.session_state.user.get("Name","Learner")
    done=len(st.session_state.completed_days)
    xp=st.session_state.xp
    streak=_streak(st.session_state.completed_days)
    level=_get_level(xp)
    day=datetime.date.today().timetuple().tm_yday
    mantra,mantra_en=MANTRAS[day%len(MANTRAS)]

    st.markdown(f"""<div class="hero">
      <div style="font-size:3.5rem;margin-bottom:4px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.4));">🇩🇪</div>
      <div class="hero-title">Willkommen, {name}!</div>
      <div class="hero-sub"><em>{mantra}</em><br><span style="font-size:.82rem;color:#555;">{mantra_en}</span></div>
      <div class="hero-pills">
        <span class="pill active">⭐ {xp} XP</span>
        <span class="pill active">🔥 {streak} day streak</span>
        <span class="pill active">🎖️ {level}</span>
        <span class="pill">Day {min(done+1,90)}/90</span>
        <span class="pill">{"🟢 AI On" if has_groq() else "⚪ AI Off"}</span>
      </div>
    </div>""",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("📅 Current Day",f"{min(done+1,90)}")
    c2.metric("⭐ Total XP",f"{xp:,}")
    c3.metric("🔥 Streak",f"{streak} days")
    c4.metric("✅ Completed",f"{done}/90")

    if PLOTLY_OK:
        st.markdown("<br>",unsafe_allow_html=True)
        ch1,ch2,ch3=st.columns(3)
        with ch1:
            f=chart_gauge(done)
            if f: st.plotly_chart(f,use_container_width=True,config={"displayModeBar":False})
        with ch2:
            f=chart_xp(st.session_state.completed_days)
            if f: st.plotly_chart(f,use_container_width=True,config={"displayModeBar":False})
        with ch3:
            f=chart_radar(st.session_state.completed_days)
            if f: st.plotly_chart(f,use_container_width=True,config={"displayModeBar":False})
        if done>0:
            f=chart_heatmap(st.session_state.completed_days)
            if f: st.plotly_chart(f,use_container_width=True,config={"displayModeBar":False})

    st.markdown("---")
    st.markdown("### 🗺️ Phase Overview")
    cols=st.columns(3)
    for i,ph in enumerate(PHASES):
        ph_done=len([d for d in ph["days"] if d in st.session_state.completed_days])
        with cols[i]:
            st.markdown(f"""<div class="g-card {'gold' if i==0 else 'red' if i==1 else 'green'}">
              <div style="font-size:1.6rem;">{ph['emoji']}</div>
              <div style="font-weight:700;margin:4px 0;">{ph['name']}</div>
              <div style="color:var(--muted);font-size:.75rem;margin-bottom:6px;">Days {ph['days'][0]}–{ph['days'][-1]} · {ph['cefr']}</div>
              <div style="color:var(--gold);font-size:1.4rem;font-weight:700;">{ph_done}/{len(ph['days'])}</div>
            </div>""",unsafe_allow_html=True)
            st.progress(ph_done/len(ph["days"]))

    week=min(done//7,len(CULTURAL_DROPS)-1)
    drop=CULTURAL_DROPS[week]
    st.markdown("---")
    st.markdown("### 🌍 Weekly Cultural Drop")
    st.markdown(f"""<div class="g-card gold">
      <div style="font-weight:700;color:var(--gold);margin-bottom:8px;">{drop['title']}</div>
      <p style="color:#ccc;line-height:1.8;">{drop['body']}</p>
    </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: ROADMAP
# ═══════════════════════════════════════════════════════════════════════════
def page_roadmap():
    st.markdown("# 🗺️ Learning Roadmap")
    search=st.text_input("🔍 Filter",placeholder="Search topic...",label_visibility="collapsed")
    content_df=load_sheet("Content")
    for ph in PHASES:
        st.markdown(f"### {ph['emoji']} {ph['name']} — {ph['cefr']}")
        for day in ph["days"]:
            is_done=day in st.session_state.completed_days
            is_curr=_unlocked(day) and not is_done
            locked=not _unlocked(day)
            topic=f"Day {day} — {ph['name']}"
            if not content_df.empty and "Day_Number" in content_df.columns:
                r=content_df[content_df["Day_Number"].astype(str)==str(day)]
                if not r.empty and r.iloc[0].get("Topic"): topic=r.iloc[0]["Topic"]
            if search and search.lower() not in topic.lower(): continue
            sc="done" if is_done else ("current" if is_curr else "locked")
            nc="done" if is_done else ("locked" if locked else "")
            ic="✅" if is_done else ("🔒" if locked else "▶")
            cn,cb=st.columns([5,1])
            with cn:
                st.markdown(f"""<div class="day-node {sc}">
                  <div class="node-num {nc}">{day}</div>
                  <div>
                    <div style="font-weight:600;font-size:.95rem;">{topic}</div>
                    <div style="color:var(--muted);font-size:.76rem;">{ic} {'Done' if is_done else ('Locked' if locked else 'Available')} · {ph['name']}</div>
                  </div></div>""",unsafe_allow_html=True)
            with cb:
                if not locked:
                    st.markdown('<div class="gold-btn">' if is_done else '',unsafe_allow_html=True)
                    if st.button("Review" if is_done else "Open",key=f"rd_{day}"):
                        st.session_state.page="daily"; st.session_state.selected_day=day; st.rerun()
                    if is_done: st.markdown('</div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: DAILY MISSION
# ═══════════════════════════════════════════════════════════════════════════
def page_daily():
    sel=int(st.session_state.get("selected_day",len(st.session_state.completed_days)+1))
    sel=max(1,min(sel,90))
    if not _unlocked(sel): st.warning("🔒 Locked — complete the previous day first."); return
    ph=_phase(sel)
    st.markdown(f"# 📅 Day {sel}")
    st.markdown(f'<span style="background:var(--red);color:#fff;border-radius:6px;padding:2px 10px;font-size:.75rem;font-weight:600;">{ph}</span>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    content_df=load_sheet("Content"); day_row={}
    if not content_df.empty and "Day_Number" in content_df.columns:
        r=content_df[content_df["Day_Number"].astype(str)==str(sel)]
        if not r.empty: day_row=r.iloc[0].to_dict()

    topic=day_row.get("Topic",f"Day {sel} — {ph}")
    vid_id=day_row.get("Video_ID","")
    anki=day_row.get("Anki_Task","Review your Anki deck — add 10 new cards (30 min)")
    pron=day_row.get("Pronunciation_Task","Practice 3 sounds on YouGlish (30 min)")
    write=day_row.get("Writing_Task","Write 5 sentences with today's vocabulary (30 min)")
    rdtxt=day_row.get("Reading_Text","")
    ar_vid=day_row.get("Video_Link_Arabic","")

    st.markdown(f"### 📖 {topic}")
    st.markdown(play_btn_html(topic,"🔊 Topic"),unsafe_allow_html=True)

    if sel<=14 and ar_vid:
        st.markdown(f"""<div class="g-card gold">
          <strong>🌉 Arabic Bridge — Foundation Support</strong>
          <p style="color:#ccc;margin:6px 0;">Watch the Arabic explanation first:</p>
          <a href="{ar_vid}" target="_blank" style="color:var(--gold);font-weight:600;text-decoration:none;">📺 Arabic Bridge Video →</a>
        </div>""",unsafe_allow_html=True)

    if vid_id:
        st.markdown(f"""<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:16px;margin:12px 0;">
          <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;border-radius:16px;"
            src="https://www.youtube.com/embed/{vid_id}?rel=0" allowfullscreen loading="lazy"></iframe>
        </div>""",unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="g-card red">
          <strong>📺 Nicos Weg — Episode {sel}</strong>
          <p style="color:#ccc;margin:6px 0;">Follow Nico and absorb natural German.</p>
          <a href="https://www.dw.com/de/nicos-weg/s-52164" target="_blank" style="color:var(--gold);font-weight:600;text-decoration:none;">🎬 Watch on DW →</a>
        </div>""",unsafe_allow_html=True)

    if rdtxt:
        with st.expander("📖 Reading Text"):
            st.markdown(f'<div style="line-height:1.9;">{rdtxt}</div>',unsafe_allow_html=True)
            st.markdown(play_btn_html(rdtxt[:200],"🔊 Listen to Reading"),unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✅ Daily Checklist (120 min)")
    dk=f"day_{sel}"
    if dk not in st.session_state.daily_tasks:
        st.session_state.daily_tasks[dk]={"anki":False,"nicos":False,"pron":False,"write":False}
    t=st.session_state.daily_tasks[dk]
    c1,c2=st.columns(2)
    with c1:
        t["anki"]=st.checkbox(f"🃏 {anki}",value=t["anki"],key=f"ta_{sel}")
        t["nicos"]=st.checkbox("📺 Watch + shadow Nicos Weg (30 min)",value=t["nicos"],key=f"tn_{sel}")
    with c2:
        t["pron"]=st.checkbox(f"🔊 {pron}",value=t["pron"],key=f"tp_{sel}")
        t["write"]=st.checkbox(f"✍️ {write}",value=t["write"],key=f"tw_{sel}")
    st.session_state.daily_tasks[dk]=t
    cnt=sum(t.values()); st.progress(cnt/4); st.markdown(f"**{cnt}/4 tasks done**")

    if cnt==4 and sel not in st.session_state.completed_days:
        st.markdown('<div class="gold-btn">',unsafe_allow_html=True)
        if st.button(f"🏆 Complete Day {sel} — +20 XP",key=f"cmp_{sel}"):
            st.session_state.completed_days.add(sel)
            st.session_state.xp+=XP_RULES.get("complete_day",20)
            save_progress(); st.balloons(); st.success(f"🎉 Day {sel} complete!"); st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    elif sel in st.session_state.completed_days:
        st.success(f"✅ Day {sel} already completed! Ausgezeichnet! 🌟")

    st.markdown("---")
    st.markdown("### 🗂️ Today's Quick Vocabulary")
    lv="A1" if sel<=30 else ("A2" if sel<=60 else "B1")
    for e in get_random_words(3,lv): render_word_card(e,show_output=False)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════
def page_dictionary():
    st.markdown("# 📖 German Dictionary")
    st.markdown("*Search · Listen · Save · Comprehensible Input & Output Practice*")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)

    cs,cf,cl=st.columns([4,1,1])
    with cs: query=st.text_input("",placeholder="🔍 Search in German, English, or Arabic...",label_visibility="collapsed")
    with cf: flv=st.selectbox("Level",["All","A1","A2","B1"],label_visibility="collapsed")
    with cl: fcat=st.selectbox("Category",["All"]+get_all_categories(),label_visibility="collapsed")

    if st.session_state.search_history:
        chips="".join([f'<span class="hist-chip">{h}</span>' for h in st.session_state.search_history[-8:]])
        st.markdown(f'<div style="margin-bottom:10px;"><span style="color:var(--muted);font-size:.73rem;">Recent: </span>{chips}</div>',unsafe_allow_html=True)

    if query and query not in st.session_state.search_history:
        st.session_state.search_history.insert(0,query); st.session_state.search_history=st.session_state.search_history[:20]

    results=search_dictionary(query) if query else DICTIONARY[:]
    if flv!="All": results=[w for w in results if w["level"]==flv]
    if fcat!="All": results=[w for w in results if w["category"]==fcat]
    st.markdown(f"**{len(results)} words found**")

    view=st.radio("",["📖 Full Cards","🖼️ Visual Grid","📋 Table"],horizontal=True,label_visibility="collapsed")
    if view=="🖼️ Visual Grid": st.markdown(image_grid_html(results[:24]),unsafe_allow_html=True); return
    if view=="📋 Table":
        df=pd.DataFrame([{"Word":w["word"],"Level":w["level"],"AR":w["ar"],"EN":w["en"],"IPA":w.get("ipa","")} for w in results])
        st.dataframe(df,use_container_width=True); return

    for e in results[:20]:
        cc,cs2=st.columns([6,1])
        with cc: render_word_card(e,show_output=True)
        with cs2:
            already=any((w if isinstance(w,str) else w.get("word",""))==e["word"] for w in st.session_state.saved_words)
            if already: st.markdown('<div style="text-align:center;color:var(--gold);font-size:.73rem;margin-top:20px;">✅ Saved</div>',unsafe_allow_html=True)
            elif st.button("💾",key=f"sv_{e['word']}",help="Save word"):
                st.session_state.saved_words.append(e); st.session_state.xp+=XP_RULES.get("save_word",2); st.rerun()
    if len(results)>20: st.info(f"Showing 20 of {len(results)}. Refine your search.")

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: AI COPILOT
# ═══════════════════════════════════════════════════════════════════════════
def page_ai():
    st.markdown("# 🤖 AI Copilot — Klaus")
    st.markdown("*Powered by **Llama 3.3 70B** via Groq · Grammar fixer · Chat · Comprehension quizzes*")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    if not has_groq():
        st.warning("⚠️ Add `GROQ_API_KEY` to `.streamlit/secrets.toml`")
        st.code('[secrets]\nGROQ_API_KEY = "gsk_YOUR_KEY_HERE"',language="toml")

    t1,t2,t3=st.tabs(["💬 Chat","✍️ Grammar Fixer","🧪 Comprehension Quiz"])

    with t1:
        st.markdown("### Chat with Klaus")
        for msg in st.session_state.ai_messages[-20:]:
            is_u=msg["role"]=="user"
            bg="rgba(255,255,255,.04)" if is_u else "rgba(245,197,24,.05)"
            brd="rgba(255,255,255,.08)" if is_u else "rgba(245,197,24,.2)"
            nm="🧑 You" if is_u else "🤖 Klaus"
            st.markdown(f"""<div style="background:{bg};border:1px solid {brd};border-radius:12px;padding:12px 16px;margin-bottom:10px;">
              <div style="color:var(--muted);font-size:.7rem;margin-bottom:3px;">{nm}</div>
              <div style="line-height:1.7;white-space:pre-wrap;">{msg['content']}</div>
            </div>""",unsafe_allow_html=True)
        ui=st.text_input("Ask Klaus…",placeholder="e.g. What's the difference between 'seit' and 'vor'?",key="chat_inp")
        c1,c2=st.columns([4,1])
        with c1:
            if st.button("Send →",key="send_chat"):
                if ui.strip():
                    with st.spinner("Klaus is thinking…"):
                        reply=groq_chat("You are Klaus, a warm German tutor. Help students learn German. Include German examples with translations. Be concise and encouraging.",
                                       st.session_state.ai_messages,ui,600)
                    st.session_state.ai_messages.extend([{"role":"user","content":ui},{"role":"assistant","content":reply}])
                    de_sentences=re.findall(r'[A-ZÄÖÜ][a-zäöüßA-ZÄÖÜ\s,\.\!]+\.',reply)
                    if de_sentences and GTTS_OK:
                        b64=tts_b64(de_sentences[0][:100])
                        if b64: st.markdown(autoplay_html(b64),unsafe_allow_html=True)
                    st.rerun()
        with c2:
            if st.button("Clear",key="clr"): st.session_state.ai_messages=[]; st.rerun()

    with t2:
        st.markdown("### ✍️ Grammar Fixer")
        st.markdown("Write German — Klaus corrects, explains every error, and gives the grammar rule.")
        user_text=st.text_area("Your German text",height=120,key="gfix",placeholder="Ich bin gehen zum Markt gestern...")
        c1,c2=st.columns([3,1])
        with c1:
            st.markdown('<div class="gold-btn">',unsafe_allow_html=True)
            if st.button("🔍 Analyze & Fix →",key="gfix_btn",use_container_width=True):
                if user_text.strip():
                    with st.spinner("Klaus is analyzing…"):
                        result=groq_correct(user_text)
                    st.markdown("### 📝 Klaus's Feedback")
                    st.markdown(f'<div class="g-card gold"><div style="line-height:1.9;white-space:pre-wrap;">{result}</div></div>',unsafe_allow_html=True)
                    corrected=re.findall(r'\*\*(.+?)\*\*',result)
                    if corrected and GTTS_OK:
                        b64=tts_b64(corrected[0][:150])
                        if b64: st.markdown("**🔊 Hear corrected version:**"); st.markdown(autoplay_html(b64),unsafe_allow_html=True)
                    st.session_state.submissions_count+=1
                    write_row("Submissions",[st.session_state.user.get("Name",""),st.session_state.user.get("Email",""),user_text,result,datetime.datetime.now().isoformat()])
                else: st.warning("Write some German text first.")
            st.markdown('</div>',unsafe_allow_html=True)
        with c2:
            if st.button("💡 Example"):
                st.session_state["gfix"]="Ich bin gehen zum Markt gestern und kaufen ein Brot."

    with t3:
        st.markdown("### 🧪 Comprehension Quiz")
        done=len(st.session_state.completed_days)
        level="A1" if done<30 else ("A2" if done<60 else "B1")
        vocab=get_random_words(8,level)
        if st.button("🎲 Generate New Quiz",key="gen_quiz"):
            with st.spinner("Klaus is preparing your quiz…"):
                q=groq_quiz(level,vocab)
            st.session_state.quiz_state={"q":q,"answered":False,"selected":None}
        if st.session_state.quiz_state:
            q=st.session_state.quiz_state["q"]
            ans=st.session_state.quiz_state.get("answered",False)
            ge=q.get("german_example","")
            aud_html=play_btn_html(ge,"🔊 Example") if ge else ""
            st.markdown(f"""<div class="g-card gold" style="margin-top:16px;">
              <div style="font-size:.72rem;color:var(--gold);text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px;">❓ Question · Level {level}</div>
              <div style="font-size:1.05rem;font-weight:600;line-height:1.6;">{q.get('question','')}</div>
              {f'<div style="margin-top:8px;">{aud_html}</div>' if aud_html else ""}
            </div>""",unsafe_allow_html=True)
            for opt in q.get("options",[]):
                if not ans:
                    if st.button(opt,key=f"qopt_{opt}"):
                        st.session_state.quiz_state["answered"]=True
                        st.session_state.quiz_state["selected"]=opt
                        if opt==q.get("answer"): st.session_state.xp+=XP_RULES.get("grammar_exercise",5)
                        st.rerun()
                else:
                    sel=st.session_state.quiz_state.get("selected","")
                    correct=q.get("answer","")
                    sty="correct" if opt==correct else ("wrong" if opt==sel and opt!=correct else "")
                    st.markdown(f'<div class="quiz-option {sty}">{opt}</div>',unsafe_allow_html=True)
            if ans:
                sel=st.session_state.quiz_state.get("selected",""); correct=q.get("answer","")
                if sel==correct: st.success(f"🎉 Richtig! +5 XP — {q.get('explanation','')}")
                else: st.error(f"❌ Answer: **{correct}** — {q.get('explanation','')}")
                if ge:
                    st.markdown(f'<div class="g-card green"><div style="font-size:.75rem;color:var(--success);">💬 Example:</div><div style="font-weight:600;margin-top:4px;">{ge}</div></div>',unsafe_allow_html=True)
                    if GTTS_OK:
                        b64=tts_b64(ge)
                        if b64: st.markdown(autoplay_html(b64),unsafe_allow_html=True)
                if st.button("Next →",key="next_q"): st.session_state.quiz_state=None; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: GAMES
# ═══════════════════════════════════════════════════════════════════════════
def page_games():
    st.markdown("# 🎮 Mini Games")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    game=st.session_state.game_state.get("active")
    done=len(st.session_state.completed_days)
    level="A1" if done<30 else ("A2" if done<60 else "B1")
    vocab=get_random_words(12,level)

    if game is None:
        c1,c2,c3=st.columns(3)
        for col,icon,name,desc,xp_str,key in [
            (c1,"🃏","Flashcard Quiz","Test vocabulary recall","+3 XP per correct","sg_fl"),
            (c2,"🔗","Word Match","Match German to meaning","+15 XP per round","sg_wm"),
            (c3,"🔀","Sentence Scramble","Rearrange words","+20 XP per solve","sg_sc"),
        ]:
            with col:
                st.markdown(f"""<div class="game-card"><div style="font-size:2.8rem;">{icon}</div>
                  <div style="font-weight:700;font-size:1.05rem;color:var(--gold);margin-top:10px;">{name}</div>
                  <div style="color:var(--muted);font-size:.8rem;margin-top:4px;">{desc}</div>
                  <div style="color:var(--red);font-size:.75rem;margin-top:8px;">{xp_str}</div></div>""",unsafe_allow_html=True)
                if st.button("Play →",key=key):
                    if key=="sg_fl":
                        random.shuffle(vocab)
                        st.session_state.game_state={"active":"flashcard","vocab":vocab,"idx":0,"score":0,"total":min(8,len(vocab))}
                    elif key=="sg_wm":
                        st.session_state.game_state={"active":"wordmatch","pairs":vocab[:6],"sel_de":None,"sel_en":None,"matched":[],"errors":0}
                    else:
                        ss=[("Ich lerne jeden Tag Deutsch.",["jeden","Deutsch.","lerne","Ich","Tag"]),
                            ("Er geht morgen in die Schule.",["in","geht","Er","Schule.","morgen","die"]),
                            ("Das Haus ist groß und schön.",["groß","Das","und","ist","schön.","Haus"])]
                        s=random.choice(ss); w=s[1][:]; random.shuffle(w)
                        st.session_state.game_state={"active":"scramble","correct":s[0],"words":w,"done":False}
                    st.session_state.games_played+=1; st.rerun()
        return

    if game=="flashcard":
        gs=st.session_state.game_state; idx=gs["idx"]
        if idx>=gs["total"]:
            earned=gs["score"]*3; st.session_state.xp+=earned
            if gs["score"]==gs["total"]: st.session_state.games_won+=1
            st.success(f"🎉 {gs['score']}/{gs['total']} correct · +{earned} XP")
            if st.button("Play Again"): st.session_state.game_state={}; st.rerun()
            return
        de,en=gs["vocab"][idx]["word"],gs["vocab"][idx]["en"]
        wrongs=[w["en"] for w in get_random_words(6,level) if w["en"]!=en][:3]
        opts=[en]+wrongs; random.shuffle(opts)
        st.markdown(f"**Card {idx+1}/{gs['total']} · Score {gs['score']}**")
        st.progress(idx/gs["total"])
        st.markdown(f"""<div class="g-card gold" style="text-align:center;padding:32px;">
          <div class="dict-word" style="font-size:3rem;">{de}</div>
          <div class="dict-ipa">{gs['vocab'][idx].get('ipa','')}</div>
          {play_btn_html(de)}
        </div>""",unsafe_allow_html=True)
        cols=st.columns(2)
        for ci,opt in enumerate(opts):
            with cols[ci%2]:
                if st.button(opt,key=f"flo_{ci}_{idx}"):
                    if opt==en: gs["score"]+=1; st.success("✅ Richtig!")
                    else: st.error(f"❌ Answer: **{en}**")
                    gs["idx"]+=1; st.session_state.game_state=gs; time.sleep(.3); st.rerun()
        if st.button("⬅ Exit",key="ex_fl"): st.session_state.game_state={}; st.rerun()

    elif game=="wordmatch":
        gs=st.session_state.game_state; pairs=gs["pairs"]; matched=gs["matched"]
        st.markdown(f"### 🔗 Word Match · {len(matched)//2}/{len(pairs)} matched · {gs['errors']} errors")
        if len(matched)==len(pairs)*2:
            earned=max(0,15-gs["errors"]*2); st.session_state.xp+=earned; st.session_state.games_won+=1
            st.success(f"🎉 All matched! +{earned} XP")
            if st.button("Play Again"): st.session_state.game_state={}; st.rerun()
            return
        en_list=[p["en"] for p in pairs]; random.seed(42); random.shuffle(en_list)
        c1,c2=st.columns(2)
        with c1:
            st.markdown("**🇩🇪 German**")
            for p in pairs:
                w=p["word"]
                if w in matched: st.markdown(f"~~{w}~~ ✅")
                elif st.button(w,key=f"de_{w}"):
                    gs["sel_de"]=w
                    if gs.get("sel_en"):
                        cen=next((x["en"] for x in pairs if x["word"]==w),None)
                        if gs["sel_en"]==cen: gs["matched"]+=[w,gs["sel_en"]]
                        else: gs["errors"]+=1
                        gs["sel_de"]=None; gs["sel_en"]=None
                    st.session_state.game_state=gs; st.rerun()
        with c2:
            st.markdown("**🇬🇧 English**")
            for w in en_list:
                if w in matched: st.markdown(f"~~{w}~~ ✅")
                elif st.button(w,key=f"en_{w}"):
                    gs["sel_en"]=w
                    if gs.get("sel_de"):
                        cen=next((x["en"] for x in pairs if x["word"]==gs["sel_de"]),None)
                        if w==cen: gs["matched"]+=[gs["sel_de"],w]
                        else: gs["errors"]+=1
                        gs["sel_de"]=None; gs["sel_en"]=None
                    st.session_state.game_state=gs; st.rerun()
        if st.button("⬅ Exit",key="ex_wm"): st.session_state.game_state={}; st.rerun()

    elif game=="scramble":
        gs=st.session_state.game_state
        st.markdown("### 🔀 Sentence Scramble")
        st.markdown(f'<div class="g-card gold"><strong>Words: {" · ".join(gs["words"])}</strong></div>',unsafe_allow_html=True)
        ans=st.text_input("Your answer:",key="scr_ans",placeholder="Type the sentence in order...")
        if st.button("✅ Check",key="chk_scr"):
            if ans.strip().lower()==gs["correct"].lower():
                st.success("🎉 Perfekt! +20 XP"); st.session_state.xp+=20; st.session_state.games_won+=1
                st.markdown(play_btn_html(gs["correct"],"🔊 Hear the sentence"),unsafe_allow_html=True)
                gs["done"]=True; st.session_state.game_state=gs
            else:
                st.error(f"❌ Correct: **{gs['correct']}**")
                st.markdown(play_btn_html(gs["correct"],"🔊 Hear it"),unsafe_allow_html=True)
        if gs.get("done") or st.button("⬅ Exit",key="ex_sc"): st.session_state.game_state={}; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: LEADERBOARD
# ═══════════════════════════════════════════════════════════════════════════
def page_leaderboard():
    st.markdown("# 🏆 Leaderboard")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    users_df=load_sheet("Users"); my_name=st.session_state.user.get("Name","")
    if not users_df.empty and "Name" in users_df.columns:
        lb=[]
        for _,row in users_df.iterrows():
            try: days=len(json.loads(str(row.get("CompletedDays","[]"))))
            except: days=0
            lb.append({"Name":row.get("Name","?"),"XP":int(row.get("XP",0))+days*20,"Streak":int(row.get("Streak",0))})
    else:
        lb=[{"Name":"Sara","XP":480,"Streak":21},{"Name":"Ahmed","XP":360,"Streak":15},
            {"Name":"Layla","XP":280,"Streak":11},
            {"Name":my_name,"XP":st.session_state.xp,"Streak":_streak(st.session_state.completed_days)}]
    medals=["🥇","🥈","🥉"]+["🏅"]*100
    t1,t2=st.tabs(["⭐ XP Ranking","🔥 Streak Ranking"])
    for tab,key,label in [(t1,"XP","⭐ {v}"),(t2,"Streak","🔥 {v} days")]:
        with tab:
            for i,u in enumerate(sorted(lb,key=lambda x:x[key],reverse=True)):
                is_you=u["Name"]==my_name
                brd=f"border:2px solid var(--{'gold' if key=='XP' else 'red'})!important;" if is_you else ""
                you='<span style="background:var(--gold);color:#000;border-radius:4px;padding:1px 7px;font-size:.66rem;font-weight:700;margin-left:6px;">YOU</span>' if is_you else ""
                st.markdown(f"""<div class="lb-row" style="{brd}">
                  <span class="lb-rank">{medals[i]}</span>
                  <span class="lb-name">{u['Name']}{you}</span>
                  <span class="lb-xp">{label.format(v=u[key])}</span>
                </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: PHONETICS LAB
# ═══════════════════════════════════════════════════════════════════════════
def page_phonetics():
    st.markdown("# 🔬 Phonetics Lab")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    cols=st.columns(3)
    for i,ph in enumerate(PHONETICS):
        with cols[i%3]:
            ex=", ".join(ph.get("example_words",[]))
            st.markdown(f"""<div class="g-card gold" style="text-align:center;margin-bottom:14px;">
              <div style="font-size:2.8rem;color:var(--gold);font-weight:900;font-family:'Playfair Display',serif;">{ph['sym']}</div>
              <div style="font-weight:700;">{ph['name']}</div>
              <div style="color:var(--muted);font-size:.75rem;font-style:italic;">{ph.get('ipa','')}</div>
              <div style="color:#ccc;font-size:.8rem;margin:6px 0;">{ph.get('desc','')}</div>
              <div style="color:var(--gold2);font-size:.76rem;">{ex}</div>
              {play_btn_html(ph['sym'],"🔊 Listen")}
              <br><br>
              <a href="https://www.youtube.com/watch?v={ph.get('yt','')}" target="_blank"
                 style="color:var(--red);font-size:.76rem;text-decoration:none;">▶ YouTube Guide</a>
            </div>""",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 👂 Minimal Pairs Practice")
    for a,b,meaning in MINIMAL_PAIRS:
        st.markdown(f"""<div style="display:flex;align-items:center;background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:12px;padding:12px 18px;margin-bottom:8px;gap:14px;flex-wrap:wrap;">
          <span style="font-size:1.05rem;color:var(--gold);font-weight:700;">{a}</span>
          {play_btn_html(a,f"🔊 {a}")}
          <span style="color:#555;">vs</span>
          <span style="font-size:1.05rem;color:var(--red);font-weight:700;">{b}</span>
          {play_btn_html(b,f"🔊 {b}")}
          <span style="color:var(--muted);font-size:.8rem;margin-left:auto;">{meaning}</span>
        </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: RESOURCES
# ═══════════════════════════════════════════════════════════════════════════
def page_resources():
    st.markdown("# 📚 Resource Library")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    if not RESOURCES: st.info("Resources will appear here."); return
    cats=sorted(set(r["cat"] for r in RESOURCES))
    for tab,cat in zip(st.tabs(cats),cats):
        with tab:
            for r in [x for x in RESOURCES if x["cat"]==cat]:
                st.markdown(f"""<a href="{r['url']}" target="_blank"
                  style="display:block;background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);
                  border-radius:12px;padding:14px 18px;margin-bottom:10px;color:var(--text);text-decoration:none;transition:border-color .2s;"
                  onmouseover="this.style.borderColor='rgba(245,197,24,.3)'" onmouseout="this.style.borderColor='rgba(255,255,255,.1)'">
                  <strong>{r['name']}</strong><br>
                  <span style="color:var(--muted);font-size:.78rem;">{r.get('desc','')} · {r['url']}</span>
                </a>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: SAVED WORDS
# ═══════════════════════════════════════════════════════════════════════════
def page_saved():
    st.markdown("# 💾 My Saved Words")
    st.markdown(f"*{len(st.session_state.saved_words)} words saved*")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    if not st.session_state.saved_words:
        st.info("No saved words yet. Use 💾 in the Dictionary."); return
    cv,cc=st.columns([4,1])
    with cv: view=st.radio("",["📖 Cards","🖼️ Visual Grid","📋 Table"],horizontal=True,label_visibility="collapsed")
    with cc:
        if st.button("🗑️ Clear All"): st.session_state.saved_words=[]; st.rerun()
    entries=[w for w in st.session_state.saved_words if isinstance(w,dict) and w.get("word")]
    if view=="🖼️ Visual Grid": st.markdown(image_grid_html(entries),unsafe_allow_html=True)
    elif view=="📋 Table":
        df=pd.DataFrame([{"Word":w["word"],"Level":w.get("level",""),"AR":w.get("ar",""),"EN":w.get("en","")} for w in entries])
        st.dataframe(df,use_container_width=True)
    else:
        for e in entries: render_word_card(e,show_output=False)

# ═══════════════════════════════════════════════════════════════════════════
#  PAGE: ADMIN
# ═══════════════════════════════════════════════════════════════════════════
def page_admin():
    st.markdown('<span class="admin-badge">⚙️ ADMIN</span>',unsafe_allow_html=True)
    st.markdown("# Mission Control")
    st.markdown('<div class="flag-bar"></div>',unsafe_allow_html=True)
    t1,t2,t3,t4,t5=st.tabs(["📋 Add Mission","👥 Students","🏆 Leaderboard","📝 Submissions","📊 Analytics"])

    with t1:
        st.markdown("### ➕ Add Daily Mission")
        c1,c2=st.columns(2)
        with c1:
            dnum=st.number_input("Day",1,90,1,key="adm_d"); phase=st.selectbox("Phase",["Foundation","Construction","Activation"],key="adm_ph")
            topic=st.text_input("Topic",key="adm_t"); vidid=st.text_input("YouTube Video ID",key="adm_v"); arlnk=st.text_input("Arabic Bridge URL",key="adm_a")
        with c2:
            anki=st.text_area("Anki Task",height=70,key="adm_anki"); pron=st.text_area("Pronunciation",height=70,key="adm_pron")
            wrt=st.text_area("Writing Task",height=70,key="adm_wrt"); rdtxt=st.text_area("Reading Text",height=70,key="adm_rd")
        st.markdown('<div class="gold-btn">',unsafe_allow_html=True)
        if st.button("💾 Save",key="adm_save"):
            if write_row("Content",[dnum,phase,topic,arlnk,vidid,anki,pron,wrt,rdtxt]): st.success(f"Day {dnum} saved!")
            else: st.error("Write failed — check Google Sheets connection.")
        st.markdown('</div>',unsafe_allow_html=True)
        df=load_sheet("Content")
        if not df.empty: st.dataframe(df,use_container_width=True)

    with t2:
        df=load_sheet("Users")
        if not df.empty:
            st.dataframe(df.drop(columns=["Password"],errors="ignore"),use_container_width=True)
            st.markdown(f"**Total: {len(df)} students**")
        else: st.info("No students yet or no Sheets connection.")

    with t3:
        df=load_sheet("Users")
        if not df.empty and "XP" in df.columns:
            st.dataframe(df[["Name","XP","Streak"]].sort_values("XP",ascending=False),use_container_width=True)

    with t4:
        df=load_sheet("Submissions")
        if not df.empty: st.dataframe(df,use_container_width=True)
        else: st.info("No submissions yet.")

    with t5:
        st.markdown("### 📊 Analytics")
        df=load_sheet("Users")
        st.metric("Total Users",len(df) if not df.empty else 0)
        if PLOTLY_OK and not df.empty and "XP" in df.columns:
            fig=px.bar(df.sort_values("XP",ascending=False).head(10),x="Name",y="XP",
                       color_discrete_sequence=["#f5c518"],template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                              font={"color":"#f8f5ef"},height=300,title="Top 10 by XP")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# ═══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown("""<div style="text-align:center;padding:16px 0 20px;">
          <div style="font-size:2.4rem;">🇩🇪</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.05rem;background:linear-gradient(135deg,#f5c518,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;margin-top:4px;">German Mastery Camp</div>
          <div style="color:#444;font-size:.7rem;">90-Day Intensive · v4.0</div>
        </div>""",unsafe_allow_html=True)

        if st.session_state.user:
            name=st.session_state.user.get("Name","Learner")
            done=len(st.session_state.completed_days); xp=st.session_state.xp
            streak=_streak(st.session_state.completed_days); level=_get_level(xp)
            adm='<span style="background:#f5c518;color:#000;border-radius:4px;padding:1px 6px;font-size:.62rem;font-weight:700;">ADMIN</span>' if st.session_state.is_admin else ""
            st.markdown(f"""<div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:12px;text-align:center;margin-bottom:14px;">
              <div style="font-size:1.5rem;">{"⚙️" if st.session_state.is_admin else "👤"}</div>
              <div style="font-weight:600;font-size:.9rem;">{name} {adm}</div>
              <div style="color:#555;font-size:.7rem;margin-top:2px;">{level} · ⭐ {xp} XP</div>
            </div>""",unsafe_allow_html=True)

        st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,.06);margin:4px 0 8px;">',unsafe_allow_html=True)

        pages={"🏠 Home":"home","🗺️ Roadmap":"roadmap","📅 Daily Mission":"daily",
               "📖 Dictionary":"dictionary","💾 Saved Words":"saved","🤖 AI Copilot":"ai",
               "🎮 Games":"games","🏆 Leaderboard":"leaderboard","🔬 Phonetics":"phonetics","📚 Resources":"resources"}
        if st.session_state.is_admin: pages["⚙️ Admin Panel"]="admin"

        for label,key in pages.items():
            active=st.session_state.page==key
            st.markdown(f'<div style="background:{"rgba(245,197,24,.07)" if active else "transparent"};border:{"1px solid rgba(245,197,24,.22)" if active else "1px solid transparent"};border-radius:8px;margin-bottom:2px;">',unsafe_allow_html=True)
            if st.button(label,key=f"nav_{key}",use_container_width=True):
                st.session_state.page=key; st.rerun()
            st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,.06);margin:8px 0;">',unsafe_allow_html=True)
        done=len(st.session_state.completed_days)
        st.markdown(f"**{done}/90 days**"); st.progress(done/90)
        streak=_streak(st.session_state.completed_days)
        st.markdown(f'<div style="display:flex;justify-content:space-between;color:#555;font-size:.76rem;"><span>🔥 {streak}</span><span>⭐ {st.session_state.xp} XP</span><span>{"🟢 AI" if has_groq() else "⚪ AI"}</span></div>',unsafe_allow_html=True)
        st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,.06);margin:8px 0;">',unsafe_allow_html=True)
        st.markdown('<div class="ghost-btn">',unsafe_allow_html=True)
        if st.button("🚪 Sign Out",use_container_width=True,key="so"):
            save_progress()
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ═══════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_auth()
else:
    sidebar()
    pg=st.session_state.page
    if   pg=="home":        page_home()
    elif pg=="roadmap":     page_roadmap()
    elif pg=="daily":       page_daily()
    elif pg=="dictionary":  page_dictionary()
    elif pg=="saved":       page_saved()
    elif pg=="ai":          page_ai()
    elif pg=="games":       page_games()
    elif pg=="leaderboard": page_leaderboard()
    elif pg=="phonetics":   page_phonetics()
    elif pg=="resources":   page_resources()
    elif pg=="admin":
        if st.session_state.is_admin: page_admin()
        else: st.error("🔒 Admin access required.")
    else: page_home()
    st.markdown('<div style="text-align:center;color:#333;font-size:.7rem;padding:20px 0 10px;">🇩🇪 German Mastery Camp v4.0 · Viel Erfolg!</div>',unsafe_allow_html=True)
