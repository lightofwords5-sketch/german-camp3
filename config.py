# ═══════════════════════════════════════════════════════════════════
#  config.py  —  German Mastery Camp  v3.0
#  Central Config: API · DB · Bilingual UI · Theme CSS · Dictionary
# ═══════════════════════════════════════════════════════════════════

import streamlit as st
import urllib.parse

# ────────────────────────────────────────────────────────────────────
#  1. APP IDENTITY
# ────────────────────────────────────────────────────────────────────
APP_NAME      = "German Mastery Camp"
APP_TAGLINE   = "Learning is living — not just memorizing."
APP_VERSION   = "3.0.0"
APP_EMOJI     = "🇩🇪"
CAMP_DURATION = 90

# ────────────────────────────────────────────────────────────────────
#  2. API SETUP  —  safe, no KeyError crashes
# ────────────────────────────────────────────────────────────────────
def _secret(key: str, fallback: str = "") -> str:
    try:
        return st.secrets[key]
    except Exception:
        return fallback

def get_anthropic_key() -> str:
    return _secret("anthropic_api_key")

def get_openai_key() -> str:
    return _secret("openai_api_key")

def get_admin_password() -> str:
    return _secret("admin_password", "admin1234")

def is_api_configured(provider: str = "anthropic") -> bool:
    key = get_anthropic_key() if provider == "anthropic" else get_openai_key()
    return bool(key) and not key.startswith("sk-xxx") and key != ""

def get_ai_provider() -> str:
    if is_api_configured("anthropic"): return "anthropic"
    if is_api_configured("openai"):    return "openai"
    return "none"

# ────────────────────────────────────────────────────────────────────
#  3. DATABASE LINKS  —  Google Sheets per-tab
# ────────────────────────────────────────────────────────────────────
def get_sheet_id() -> str:
    return _secret("sheet_id", "")

def get_gcp_credentials() -> dict | None:
    try:
        return dict(st.secrets["gcp_service_account"])
    except Exception:
        return None

SHEET_TABS = {
    "users":           "Users",
    "content":         "Content",
    "user_vocabulary": "User_Vocabulary",
    "dictionary":      "Dictionary",
    "submissions":     "Submissions",
    "missions":        "Missions",
}

# ────────────────────────────────────────────────────────────────────
#  4. COLORS
# ────────────────────────────────────────────────────────────────────
COLORS = {
    "black":   "#0d0d0d", "red":    "#cc0000", "gold":   "#f5c518",
    "gold2":   "#d4a017", "white":  "#f8f5ef", "card":   "#1a1a1a",
    "card2":   "#222222", "border": "#2e2e2e", "muted":  "#777777",
    "success": "#22c55e", "info":   "#3b82f6", "warning":"#f59e0b",
    "light_bg":"#f8f5ef", "light_card":"#ffffff","light_border":"#e5e5e5","light_text":"#1a1a1a",
}

# ────────────────────────────────────────────────────────────────────
#  5. THEME CSS  —  dark / light mode
# ────────────────────────────────────────────────────────────────────
def get_theme_css(mode: str = "dark") -> str:
    is_dark = mode != "light"
    bg     = COLORS["black"]    if is_dark else COLORS["light_bg"]
    card   = COLORS["card"]     if is_dark else COLORS["light_card"]
    border = COLORS["border"]   if is_dark else COLORS["light_border"]
    text   = COLORS["white"]    if is_dark else COLORS["light_text"]
    muted  = "#777"             if is_dark else "#999"
    sidebar = "linear-gradient(180deg,#0d0d0d 0%,#1a0000 100%)" if is_dark else "linear-gradient(180deg,#fff5f5 0%,#fff 100%)"
    R,G = COLORS['red'], COLORS['gold']
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');
:root{{--black:#0d0d0d;--red:{R};--gold:{G};--gold2:{COLORS['gold2']};--white:{COLORS['white']};
      --bg:{bg};--card:{card};--border:{border};--text:{text};--muted:{muted};
      --success:{COLORS['success']};--info:{COLORS['info']};}}
html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;background:{bg}!important;color:{text}!important;}}
h1,h2,h3{{font-family:'Playfair Display',serif!important;}}
h1{{color:{G}!important;font-size:2.2rem!important;}}
h2{{color:{R}!important;}} h3{{color:{COLORS['gold2']}!important;}}
[data-testid="stSidebar"]{{background:{sidebar}!important;border-right:2px solid {R}!important;}}
[data-testid="stSidebar"] *{{color:{text}!important;}}
[data-testid="stMetric"]{{background:{card}!important;border:1px solid {border}!important;border-radius:12px!important;padding:16px!important;}}
[data-testid="stMetricValue"]{{color:{G}!important;font-size:1.8rem!important;}}
[data-testid="stMetricLabel"]{{color:{muted}!important;}}
[data-testid="stProgressBar"]>div>div{{background:linear-gradient(90deg,{R},{G})!important;}}
.stButton>button{{background:linear-gradient(135deg,{R},#8b0000)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:600!important;transition:all .15s!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(204,0,0,.4)!important;}}
.gold-btn .stButton>button{{background:linear-gradient(135deg,{G},{COLORS['gold2']})!important;color:#000!important;}}
.green-btn .stButton>button{{background:linear-gradient(135deg,#16a34a,#166534)!important;color:#fff!important;}}
[data-testid="stTabs"] button{{color:{muted}!important;font-weight:500!important;}}
[data-testid="stTabs"] button[aria-selected="true"]{{color:{G}!important;border-bottom:2px solid {G}!important;}}
[data-testid="stSelectbox"]>div,[data-testid="stTextInput"]>div>div,[data-testid="stTextArea"]>div>div{{background:{card}!important;border:1px solid {border}!important;color:{text}!important;border-radius:8px!important;}}
.gmc-card{{background:{card};border:1px solid {border};border-radius:14px;padding:20px 24px;margin-bottom:14px;}}
.gmc-card.gold{{border-left:4px solid {G};}} .gmc-card.red{{border-left:4px solid {R};}}
.gmc-card.green{{border-left:4px solid {COLORS['success']};}} .gmc-card.flag{{background:linear-gradient(135deg,{card} 60%,#1a0000 100%);border:1px solid {R};}}
.mantra-box{{background:linear-gradient(135deg,#1a0a00,#1a1a00);border:1px solid {G};border-radius:14px;padding:22px 28px;text-align:center;font-size:1.1rem;font-style:italic;color:{G};font-family:'Playfair Display',serif;margin-bottom:22px;}}
.flag-bar{{height:6px;background:linear-gradient(90deg,#000 33%,{R} 33% 66%,{G} 66%);margin-bottom:20px;border-radius:3px;}}

/* ── DICTIONARY CARD ── */
.dict-card{{background:{card};border:1px solid {border};border-radius:16px;padding:20px;margin-bottom:12px;transition:border-color .2s;position:relative;overflow:hidden;}}
.dict-card:hover{{border-color:{G};}}
.dict-card::before{{content:'';position:absolute;top:0;left:0;width:4px;height:100%;background:linear-gradient(180deg,{R},{G});}}
.dict-word{{font-family:'Playfair Display',serif;font-size:1.8rem;color:{G};font-weight:700;}}
.dict-phonetic{{color:{muted};font-size:.85rem;font-style:italic;margin-top:2px;}}
.dict-translations{{display:flex;gap:12px;margin:10px 0;flex-wrap:wrap;}}
.dict-trans-ar{{background:#1a0500;border:1px solid {R};border-radius:8px;padding:4px 12px;font-size:.9rem;color:{G};direction:rtl;}}
.dict-trans-en{{background:#001a0a;border:1px solid {COLORS['success']};border-radius:8px;padding:4px 12px;font-size:.9rem;color:{COLORS['success']};}}
.dict-example{{background:#111;border-radius:8px;padding:12px 14px;margin-top:10px;}}
.dict-example-de{{font-size:1rem;color:{text};font-weight:500;line-height:1.7;}}
.dict-example-ar{{font-size:.88rem;color:{muted};direction:rtl;margin-top:4px;}}
.dict-example-en{{font-size:.85rem;color:{muted};margin-top:2px;font-style:italic;}}
.dict-audio-btn{{background:linear-gradient(135deg,{R},#8b0000);color:#fff;border:none;border-radius:8px;padding:6px 14px;font-size:.82rem;font-weight:600;cursor:pointer;transition:all .15s;margin-top:8px;}}
.dict-audio-btn:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(204,0,0,.4);}}
.input-box{{background:{card};border:1px solid {COLORS['info']};border-radius:10px;padding:14px;margin-top:8px;}}
.output-box{{background:{card};border:1px solid {COLORS['success']};border-radius:10px;padding:14px;margin-top:8px;}}
.day-node{{display:flex;align-items:center;gap:14px;background:{card};border:1px solid {border};border-radius:12px;padding:14px 18px;margin-bottom:8px;}}
.day-node.done{{border-left:4px solid {COLORS['success']};}} .day-node.current{{border-left:4px solid {G};background:#1a1800;}} .day-node.locked{{opacity:.4;pointer-events:none;}}
.node-num{{background:{R};color:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0;}}
.node-num.done{{background:{COLORS['success']};}} .node-num.locked{{background:#333;}}
.lb-row{{display:flex;align-items:center;background:{card};border:1px solid {border};border-radius:10px;padding:12px 18px;margin-bottom:8px;gap:12px;}}
.lb-rank{{font-size:1.3rem;width:32px;}} .lb-name{{flex:1;font-weight:600;}} .lb-xp{{color:{G};font-weight:700;}}
.game-card{{background:linear-gradient(135deg,{card},#0d0d0d);border:1px solid {G};border-radius:16px;padding:28px;text-align:center;cursor:pointer;transition:all .2s;}}
.game-card:hover{{border-color:{R};transform:translateY(-4px);box-shadow:0 12px 32px rgba(204,0,0,.25);}}
.admin-badge{{display:inline-block;background:{G};color:#000;border-radius:6px;padding:2px 10px;font-size:.75rem;font-weight:700;}}
div[data-testid="column"]{{padding:6px!important;}}
@media(max-width:768px){{.dict-translations{{flex-direction:column;}}.dict-word{{font-size:1.4rem;}}h1{{font-size:1.6rem!important;}}}}
</style>"""

# ────────────────────────────────────────────────────────────────────
#  6. BILINGUAL UI TEXT
# ────────────────────────────────────────────────────────────────────
UI_TEXT = {
    "nav_home":        {"ar":"الرئيسية",         "en":"Home"},
    "nav_roadmap":     {"ar":"خريطة التعلم",      "en":"Roadmap"},
    "nav_daily":       {"ar":"مهمة اليوم",        "en":"Daily Mission"},
    "nav_dictionary":  {"ar":"القاموس",           "en":"Dictionary"},
    "nav_ai":          {"ar":"المساعد الذكي",     "en":"AI Copilot"},
    "nav_games":       {"ar":"الألعاب",           "en":"Games"},
    "nav_leaderboard": {"ar":"المتصدرين",         "en":"Leaderboard"},
    "nav_phonetics":   {"ar":"مختبر النطق",       "en":"Phonetics Lab"},
    "nav_resources":   {"ar":"المصادر",           "en":"Resources"},
    "nav_mentor":      {"ar":"المرشد الثقافي",    "en":"Mentor Corner"},
    "nav_admin":       {"ar":"لوحة التحكم",       "en":"Admin Panel"},
    "sign_in":         {"ar":"تسجيل الدخول",     "en":"Sign In"},
    "sign_up":         {"ar":"إنشاء حساب",       "en":"Create Account"},
    "sign_out":        {"ar":"تسجيل الخروج",     "en":"Sign Out"},
    "email":           {"ar":"البريد الإلكتروني","en":"Email"},
    "password":        {"ar":"كلمة المرور",      "en":"Password"},
    "full_name":       {"ar":"الاسم الكامل",     "en":"Full Name"},
    "welcome_back":    {"ar":"مرحباً بعودتك",   "en":"Welcome back"},
    "invalid_creds":   {"ar":"بيانات خاطئة",    "en":"Invalid credentials"},
    "days_done":       {"ar":"الأيام المكتملة", "en":"Days Done"},
    "current_streak":  {"ar":"الأيام المتتالية","en":"Current Streak"},
    "total_xp":        {"ar":"مجموع النقاط",    "en":"Total XP"},
    "current_day":     {"ar":"اليوم الحالي",    "en":"Current Day"},
    "complete_day":    {"ar":"أكمل اليوم ✅",    "en":"Complete Day ✅"},
    "day_locked":      {"ar":"🔒 مقفل — أكمل اليوم السابق أولاً","en":"🔒 Locked — complete the previous day first"},
    "dict_title":      {"ar":"القاموس الألماني","en":"German Dictionary"},
    "dict_search":     {"ar":"ابحث عن كلمة...","en":"Search for a word..."},
    "dict_listen":     {"ar":"🔊 استمع",        "en":"🔊 Listen"},
    "dict_save":       {"ar":"💾 احفظ الكلمة", "en":"💾 Save Word"},
    "dict_saved":      {"ar":"✅ محفوظة",       "en":"✅ Saved"},
    "dict_input":      {"ar":"📥 مدخلات — استوعب","en":"📥 Comprehensible Input"},
    "dict_output":     {"ar":"📤 مخرجات — أنتج","en":"📤 Output Practice"},
    "ai_title":        {"ar":"المساعد الذكي كلاوس","en":"AI Copilot Klaus"},
    "ai_thinking":     {"ar":"كلاوس يفكر...",  "en":"Klaus is thinking..."},
    "ai_placeholder":  {"ar":"اسأل أي سؤال عن الألمانية...","en":"Ask anything about German..."},
    "ai_fix_title":    {"ar":"مصحح القواعد",   "en":"Grammar Fixer"},
    "ai_fix_btn":      {"ar":"🔍 صحح وشرح",    "en":"🔍 Analyze & Fix"},
    "ai_no_key":       {"ar":"⚠️ مفتاح الـ AI غير مضبوط — أضفه في secrets.toml","en":"⚠️ AI key not configured — add it to secrets.toml"},
    "games_title":     {"ar":"الألعاب التعليمية","en":"Learning Games"},
    "play":            {"ar":"العب →",          "en":"Play →"},
    "correct":         {"ar":"✅ صحيح!",        "en":"✅ Correct!"},
    "wrong":           {"ar":"❌ خطأ",           "en":"❌ Wrong"},
    "game_over":       {"ar":"🎉 انتهت اللعبة!","en":"🎉 Game Over!"},
    "mantra_label":    {"ar":"مقولة اليوم",     "en":"Mantra of the Day"},
    "cultural_drop":   {"ar":"الإلقاء الثقافي الأسبوعي","en":"Weekly Cultural Drop"},
}

def t(key: str, lang: str = "ar") -> str:
    entry = UI_TEXT.get(key, {})
    return entry.get(lang, entry.get("en", key))

# ────────────────────────────────────────────────────────────────────
#  7. DICTIONARY  —  Top 100 German Words (extendable to 500+)
#     Each entry: word · gender · plural · level · category
#                 ar · en · ipa · example_de · example_ar · example_en
#                 audio_url · input_image_keyword · output_prompt_ar
# ────────────────────────────────────────────────────────────────────
def _audio(word: str) -> str:
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(word)}&tl=de"

def _card(w,g,pl,lv,cat,ar,en,ipa,ex_de,ex_ar,ex_en,img,prompt):
    return {"word":w,"gender":g,"plural":pl,"level":lv,"category":cat,
            "ar":ar,"en":en,"ipa":ipa,
            "example_de":ex_de,"example_ar":ex_ar,"example_en":ex_en,
            "audio_url":_audio(w),"input_image_keyword":img,"output_prompt_ar":prompt}

DICTIONARY = [
    _card("Haus","das","Häuser","A1","🏠 Zuhause","بيت","house","[haʊs]",
          "Das Haus ist groß und hat einen Garten.",
          "البيت كبير وله حديقة.","The house is big and has a garden.",
          "house exterior Germany","صف البيت الذي تراه في الصورة."),
    _card("Wasser","das","-","A1","🍽️ Essen","ماء","water","[ˈvasɐ]",
          "Ich trinke jeden Morgen ein Glas Wasser.",
          "أشرب كوب ماء كل صباح.","I drink a glass of water every morning.",
          "glass of water clear","اكتب جملة عما تشربه في الصباح."),
    _card("Familie","die","Familien","A1","👨‍👩‍👧 Familie","عائلة","family","[faˈmiːliə]",
          "Meine Familie ist sehr groß — wir sind sieben Personen.",
          "عائلتي كبيرة جداً — نحن سبعة أشخاص.","My family is very large — there are seven of us.",
          "family portrait smiling","صف عائلتك: كم عددهم وماذا يعملون."),
    _card("Zeit","die","Zeiten","A1","⏰ Zeit","وقت","time","[tsaɪt]",
          "Ich habe heute keine Zeit.",
          "ليس لدي وقت اليوم.","I have no time today.",
          "clock watch time","كم ساعة تتعلم الألمانية يومياً؟"),
    _card("Geld","das","-","A1","💰 Alltag","مال","money","[ɡɛlt]",
          "Ich habe nicht viel Geld, aber ich bin glücklich.",
          "ليس لدي مال كثير لكنني سعيد.","I don't have a lot of money, but I'm happy.",
          "euro coins banknotes","اكتب جملة عما تشتريه بمصروفك."),
    _card("Stadt","die","Städte","A1","🏙️ Orte","مدينة","city","[ʃtat]",
          "Berlin ist eine sehr interessante Stadt.",
          "برلين مدينة مثيرة للاهتمام.","Berlin is a very interesting city.",
          "Berlin city skyline","صف مدينتك: كبيرة أم صغيرة؟"),
    _card("Schule","die","Schulen","A1","📚 Bildung","مدرسة","school","[ˈʃuːlə]",
          "Die Schule beginnt um acht Uhr morgens.",
          "تبدأ المدرسة الساعة الثامنة صباحاً.","School starts at eight in the morning.",
          "German school classroom","اكتب عن مدرستك أو جامعتك."),
    _card("Freund","der","Freunde","A1","👥 Soziales","صديق","friend","[fʁɔʏnt]",
          "Mein bester Freund heißt Omar.",
          "اسم صديقي المقرب عمر.","My best friend's name is Omar.",
          "two friends laughing","صف صديقك المفضل في جملتين."),
    _card("Essen","das","-","A1","🍽️ Essen","طعام","food / to eat","[ˈɛsən]",
          "Das Essen in Deutschland ist sehr gut.",
          "الطعام في ألمانيا لذيذ جداً.","The food in Germany is very good.",
          "German food traditional","صف وجبتك المفضلة."),
    _card("Buch","das","Bücher","A1","📚 Bildung","كتاب","book","[buːx]",
          "Ich lese jeden Abend ein Buch.",
          "أقرأ كتاباً كل مساء.","I read a book every evening.",
          "open book reading light","اكتب عن آخر كتاب قرأته."),
    _card("Auto","das","Autos","A1","🚗 Verkehr","سيارة","car","[ˈaʊto]",
          "Mein Vater hat ein neues Auto.",
          "والدي لديه سيارة جديدة.","My father has a new car.",
          "German car BMW Mercedes","كيف تتنقل يومياً؟"),
    _card("Mann","der","Männer","A1","👥 Soziales","رجل","man","[man]",
          "Der Mann liest eine Zeitung im Park.",
          "الرجل يقرأ جريدة في الحديقة.","The man reads a newspaper in the park.",
          "man reading park bench","صف شخصاً تراه الآن."),
    _card("Frau","die","Frauen","A1","👥 Soziales","امرأة / السيدة","woman / Mrs.","[fʁaʊ]",
          "Die Frau arbeitet als Ärztin.",
          "المرأة تعمل طبيبة.","The woman works as a doctor.",
          "woman professional confident","اكتب عن امرأة مؤثرة في حياتك."),
    _card("Kind","das","Kinder","A1","👨‍👩‍👧 Familie","طفل","child","[kɪnt]",
          "Das Kind spielt im Garten.",
          "الطفل يلعب في الحديقة.","The child plays in the garden.",
          "child playing garden happy","صف طفلاً تعرفه."),
    _card("Tag","der","Tage","A1","⏰ Zeit","يوم","day","[taːk]",
          "Guten Tag! Wie geht es Ihnen heute?",
          "مرحباً! كيف حالك اليوم؟","Good day! How are you today?",
          "sunny day Germany park","صف يومك المثالي."),
    _card("Jahr","das","Jahre","A1","⏰ Zeit","سنة","year","[jaːɐ]",
          "Ich lerne seit einem Jahr Deutsch.",
          "أتعلم الألمانية منذ سنة.","I have been learning German for a year.",
          "calendar year planner desk","ما الذي تعلمته هذا العام؟"),
    _card("Sprache","die","Sprachen","A1","📚 Bildung","لغة","language","[ˈʃpʁaːxə]",
          "Deutsch ist eine schöne Sprache.",
          "اللغة الألمانية لغة جميلة.","German is a beautiful language.",
          "world languages flags diversity","لماذا تتعلم اللغة الألمانية؟"),
    _card("Arbeit","die","Arbeiten","A1","💼 Beruf","عمل","work / job","[ˈaʁbaɪt]",
          "Die Arbeit beginnt um neun Uhr.",
          "يبدأ العمل الساعة التاسعة.","Work starts at nine o'clock.",
          "office workplace laptop","صف ما تريد أن تعمله."),
    _card("Straße","die","Straßen","A1","🏙️ Orte","شارع","street","[ˈʃtʁaːsə]",
          "Ich wohne in der Hauptstraße Nummer zehn.",
          "أسكن في الشارع الرئيسي رقم عشرة.","I live at number ten, Main Street.",
          "German street cobblestone old","صف الشارع الذي تسكن فيه."),
    _card("Wetter","das","-","A1","🌤️ Natur","الطقس","weather","[ˈvɛtɐ]",
          "Das Wetter in Hamburg ist oft regnerisch.",
          "الطقس في هامبورغ ممطر في الغالب.","The weather in Hamburg is often rainy.",
          "rainy day Germany umbrella","صف الطقس اليوم في مدينتك."),
    _card("Bahnhof","der","Bahnhöfe","A2","🚗 Verkehr","محطة القطار","train station","[ˈbaːnhoːf]",
          "Der Bahnhof ist zehn Minuten zu Fuß entfernt.",
          "محطة القطار على بعد عشر دقائق مشياً.","The train station is ten minutes away on foot.",
          "Berlin Hauptbahnhof modern","صف كيف تصل إلى المحطة."),
    _card("Urlaub","der","Urlaube","A2","✈️ Reisen","إجازة","vacation / holiday","[ˈʊʁlaʊp]",
          "Im Sommer fahre ich in den Urlaub nach Österreich.",
          "في الصيف أسافر في إجازة إلى النمسا.","In summer I go on holiday to Austria.",
          "summer vacation beach mountains","أين تريد أن تقضي عطلتك؟"),
    _card("Gesundheit","die","-","A2","🏥 Gesundheit","صحة","health","[ɡəˈzʊnthaɪt]",
          "Gesundheit ist das Wichtigste im Leben.",
          "الصحة أهم شيء في الحياة.","Health is the most important thing in life.",
          "healthy lifestyle sport food","كيف تحافظ على صحتك؟"),
    _card("Krankenhaus","das","Krankenhäuser","A2","🏥 Gesundheit","مستشفى","hospital","[ˈkʁaŋkənhaʊs]",
          "Das Krankenhaus ist in der Mitte der Stadt.",
          "المستشفى في وسط المدينة.","The hospital is in the centre of the city.",
          "hospital building entrance modern","هل سبق أن زرت مستشفى؟"),
    _card("Freude","die","-","A2","😊 Gefühle","فرح","joy","[ˈfʁɔʏdə]",
          "Die Freude in seinen Augen war unbeschreiblich.",
          "الفرح في عينيه كان لا يوصف.","The joy in his eyes was indescribable.",
          "happy people celebrating joy","ما الذي يجلب لك الفرح؟"),
    _card("Hoffnung","die","Hoffnungen","B1","💭 Gedanken","أمل","hope","[ˈhɔfnʊŋ]",
          "Ich habe die Hoffnung, eines Tages in Deutschland zu leben.",
          "لدي أمل أن أعيش يوماً ما في ألمانيا.","I have the hope of living in Germany one day.",
          "sunrise hope bright future sky","ما أملك في تعلم الألمانية؟"),
    _card("Möglichkeit","die","Möglichkeiten","B1","💭 Gedanken","فرصة / إمكانية","opportunity","[ˈmøːklɪçkaɪt]",
          "Deutsch lernen eröffnet viele Möglichkeiten.",
          "تعلم الألمانية يفتح أمامك إمكانيات كثيرة.","Learning German opens up many possibilities.",
          "open door career opportunity","ما الفرص التي تتوقعها بعد الألمانية؟"),
    _card("Herausforderung","die","Herausforderungen","B1","💭 Gedanken","تحدي","challenge","[hɛˈʁaʊsfɔʁdəʁʊŋ]",
          "Das Lernen einer Fremdsprache ist eine echte Herausforderung.",
          "تعلم لغة أجنبية تحدٍّ حقيقي.","Learning a foreign language is a real challenge.",
          "climbing mountain challenge persevere","ما أكبر تحدٍّ في تعلم الألمانية؟"),
    _card("Entscheidung","die","Entscheidungen","B1","💭 Gedanken","قرار","decision","[ɛntˈʃaɪdʊŋ]",
          "Die Entscheidung, Deutsch zu lernen, war richtig.",
          "كان قرار تعلم الألمانية صحيحاً.","The decision to learn German was the right one.",
          "crossroads decision making choice","اكتب عن قرار مهم اتخذته."),
    _card("Erfahrung","die","Erfahrungen","B1","💭 Gedanken","تجربة","experience","[ɛʁˈfaːʁʊŋ]",
          "Diese Reise war eine wertvolle Erfahrung für mich.",
          "كانت هذه الرحلة تجربة قيّمة.","This trip was a valuable experience for me.",
          "travel adventure experience new place","صف تجربة مميزة في حياتك."),
    _card("Baum","der","Bäume","A1","🌤️ Natur","شجرة","tree","[baʊm]",
          "Im Park stehen viele alte Bäume.",
          "في الحديقة أشجار كثيرة وقديمة.","There are many old trees in the park.",
          "tree park autumn Germany colors","صف شجرة تراها من نافذتك."),
    _card("Meer","das","Meere","A1","🌤️ Natur","بحر","sea","[meːɐ]",
          "Im Sommer fahren wir ans Meer.",
          "في الصيف نذهب إلى البحر.","In summer we go to the sea.",
          "North Sea Germany beach waves","صف آخر زيارة للبحر."),
    _card("Brot","das","Brote","A1","🍽️ Essen","خبز","bread","[bʁoːt]",
          "Deutsches Brot ist weltberühmt.",
          "الخبز الألماني مشهور عالمياً.","German bread is world-famous.",
          "German bread varieties rye wholemeal","صف الخبز الذي تأكله مع الإفطار."),
    _card("Kaffee","der","-","A1","🍽️ Essen","قهوة","coffee","[ˈkafe]",
          "Ich trinke morgens immer einen Kaffee.",
          "أشرب دائماً قهوة في الصباح.","I always drink a coffee in the morning.",
          "coffee cup morning steam","هل تشرب القهوة؟ صف كيف تشربها."),
    _card("sein","—","-","A1","🔧 Verben","يكون","to be","[zaɪn]",
          "Ich bin Student. Du bist mein Freund.",
          "أنا طالب. أنت صديقي.","I am a student. You are my friend.",
          "identity passport person portrait","قدم نفسك في جملتين باستخدام 'ich bin'."),
    _card("haben","—","-","A1","🔧 Verben","يملك","to have","[ˈhaːbən]",
          "Ich habe einen Bruder und eine Schwester.",
          "لدي أخ وأخت.","I have a brother and a sister.",
          "person holding items possessions","اكتب ثلاثة أشياء تمتلكها."),
    _card("gehen","—","-","A1","🔧 Verben","يذهب","to go","[ˈɡeːən]",
          "Ich gehe jeden Morgen ins Café.",
          "أذهب إلى المقهى كل صباح.","I go to the café every morning.",
          "person walking street city morning","إلى أين تذهب كل يوم؟"),
    _card("kommen","—","-","A1","🔧 Verben","يأتي","to come","[ˈkɔmən]",
          "Woher kommst du? — Ich komme aus Ägypten.",
          "من أين أنت؟ — أنا من مصر.","Where are you from? — I'm from Egypt.",
          "arrival welcome sign airport","من أين أنت وأين تسكن الآن؟"),
    _card("machen","—","-","A1","🔧 Verben","يفعل / يصنع","to make / do","[ˈmaxən]",
          "Was machst du am Wochenende?",
          "ماذا تفعل في عطلة نهاية الأسبوع؟","What do you do on the weekend?",
          "person doing hobby weekend activity","اكتب ثلاثة أشياء تفعلها في نهاية الأسبوع."),
    _card("sprechen","—","-","A1","🔧 Verben","يتحدث","to speak","[ˈʃpʁɛçən]",
          "Sprichst du Englisch? — Ja, und ich lerne Deutsch.",
          "هل تتكلم الإنجليزية؟ — نعم، وأتعلم الألمانية.","Do you speak English? — Yes, I'm learning German.",
          "people conversation talking discuss","كم لغة تتكلم؟ اكتبها بالألمانية."),
    _card("lernen","—","-","A1","🔧 Verben","يتعلم","to learn","[ˈlɛʁnən]",
          "Ich lerne jeden Tag Deutsch.",
          "أتعلم الألمانية كل يوم.","I learn German every day.",
          "student studying books desk focus","ما الذي تريد تعلمه هذا الأسبوع؟"),
    _card("können","—","-","A1","🔧 Verben","يستطيع","can / to be able to","[ˈkœnən]",
          "Ich kann gut Deutsch sprechen, aber noch nicht perfekt.",
          "أستطيع التحدث بالألمانية جيداً لكن ليس مثالياً.","I can speak German well, but not perfectly yet.",
          "superhero ability skill power","ماذا تستطيع أن تفعل الآن بالألمانية؟"),
    _card("müssen","—","-","A1","🔧 Verben","يجب","must / have to","[ˈmʏsən]",
          "Ich muss morgen früh aufstehen.",
          "يجب أن أستيقظ باكراً غداً.","I have to get up early tomorrow.",
          "alarm clock early morning wake","اكتب ثلاثة أشياء يجب أن تفعلها اليوم."),
    _card("wollen","—","-","A1","🔧 Verben","يريد","to want to","[ˈvɔlən]",
          "Ich will Deutsch lernen, um in Deutschland zu studieren.",
          "أريد تعلم الألمانية لأدرس في ألمانيا.","I want to learn German to study in Germany.",
          "person goal ambition future success","ما الذي تريد تحقيقه خلال 90 يوم؟"),
    _card("wissen","—","-","A1","🔧 Verben","يعلم / يعرف","to know (fact)","[ˈvɪsən]",
          "Ich weiß nicht, wo der Bahnhof ist.",
          "لا أعرف أين المحطة.","I don't know where the train station is.",
          "thinking person question mark knowledge","اكتب شيئاً تعرفه عن ألمانيا."),
    _card("wohnen","—","-","A1","🔧 Verben","يسكن","to live / reside","[ˈvoːnən]",
          "Ich wohne in Kairo, aber ich möchte in Berlin wohnen.",
          "أسكن في القاهرة لكنني أريد العيش في برلين.","I live in Cairo but I'd like to live in Berlin.",
          "apartment building city residential","صف مكان سكنك."),
    _card("groß","—","-","A1","📐 Adjektive","كبير / طويل","big / tall","[ɡʁoːs]",
          "Mein Bruder ist sehr groß — er ist 1,90 m.",
          "أخي طويل جداً — طوله مترٌ وتسعون سنتيمتراً.","My brother is very tall — he is 1.90 m.",
          "tall building skyscraper architecture","صف شيئاً كبيراً وشيئاً صغيراً في غرفتك."),
    _card("gut","—","-","A1","📐 Adjektive","جيد","good","[ɡuːt]",
          "Das Essen ist sehr gut. Ich esse gerne hier.",
          "الطعام جيد جداً. أحب الأكل هنا.","The food is very good. I like eating here.",
          "thumbs up approval good quality","ما أفضل شيء في يومك اليوم؟"),
    _card("schön","—","-","A1","📐 Adjektive","جميل","beautiful / nice","[ʃøːn]",
          "Das Wetter heute ist wirklich schön.",
          "الطقس اليوم جميل فعلاً.","The weather today is really beautiful.",
          "beautiful sunny landscape Germany nature","صف شيئاً جميلاً تراه من نافذتك."),
    _card("wichtig","—","-","A2","📐 Adjektive","مهم","important","[ˈvɪçtɪç]",
          "Deutsch lernen ist für meine Karriere sehr wichtig.",
          "تعلم الألمانية مهم جداً لمسيرتي المهنية.","Learning German is very important for my career.",
          "important priority highlight star","ما أهم شيء بالنسبة لك في الحياة؟"),
    _card("schwierig","—","-","A2","📐 Adjektive","صعب","difficult","[ˈʃviːʁɪç]",
          "Die deutsche Grammatik ist manchmal schwierig, aber lernbar.",
          "قواعد الألمانية صعبة أحياناً لكن يمكن تعلمها.","German grammar is sometimes difficult but learnable.",
          "climbing mountain challenge difficult hard","ما أصعب جانب في الألمانية لك؟"),
    _card("einfach","—","-","A1","📐 Adjektive","سهل / بسيط","simple / easy","[ˈaɪnfax]",
          "Diese Aufgabe ist wirklich einfach.",
          "هذا التمرين سهل فعلاً.","This task is really easy.",
          "simple easy clean minimal design","ما أسهل شيء تعلمته في الألمانية؟"),
    _card("glücklich","—","-","A1","😊 Gefühle","سعيد","happy","[ˈɡlʏklɪç]",
          "Ich bin sehr glücklich, weil ich Deutsch lerne.",
          "أنا سعيد جداً لأنني أتعلم الألمانية.","I am very happy because I am learning German.",
          "happy smiling person joyful","ما الذي يجعلك سعيداً؟"),
    _card("traurig","—","-","A1","😊 Gefühle","حزين","sad","[ˈtʁaʊʁɪç]",
          "Ich bin traurig, wenn ich keine Zeit habe.",
          "أنا حزين عندما لا يكون لدي وقت.","I am sad when I have no time.",
          "sad person reflection melancholy","متى تشعر بالحزن؟"),
    _card("müde","—","-","A1","😊 Gefühle","متعب","tired","[ˈmyːdə]",
          "Ich bin heute sehr müde — ich habe schlecht geschlafen.",
          "أنا متعب جداً اليوم — لم أنم جيداً.","I am very tired today — I slept badly.",
          "tired yawning person sleepy morning","كيف تتعافى من التعب؟"),
    _card("aufgeregt","—","-","A2","😊 Gefühle","متحمس","excited / nervous","[ˈaʊfɡəˌʁɛkt]",
          "Ich bin so aufgeregt vor meiner Deutschprüfung!",
          "أنا متحمس جداً قبل اختبار الألمانية!","I am so excited before my German exam!",
          "excited nervous student exam anticipation","متى تشعر بالتحمس؟"),
    _card("obwohl","—","-","B1","📝 Grammatik","على الرغم من أن","although","[ɔpˈvoːl]",
          "Obwohl es regnet, gehe ich spazieren.",
          "على الرغم من المطر أذهب للمشي.","Although it is raining, I go for a walk.",
          "rain walking umbrella persevere","اكتب جملة بـ 'obwohl' عن تعلم الألمانية."),
    _card("trotzdem","—","-","B1","📝 Grammatik","مع ذلك / بالرغم منه","nevertheless","[ˈtʁɔtsdəm]",
          "Ich bin müde, trotzdem lerne ich heute.",
          "أنا متعب، ومع ذلك أتعلم اليوم.","I am tired, nevertheless I study today.",
          "persistence determination keep going forward","اكتب جملة بـ 'trotzdem' تعبّر عن إصرارك."),
    _card("deshalb","—","-","B1","📝 Grammatik","لذلك","therefore / that's why","[ˈdɛshalp]",
          "Ich liebe Musik, deshalb spiele ich Gitarre.",
          "أحب الموسيقى، لذلك أعزف الغيتار.","I love music, that's why I play guitar.",
          "cause effect reason chain logic","اكتب جملة بـ 'deshalb' توضح سبب تعلمك الألمانية."),
    _card("allerdings","—","-","B1","📝 Grammatik","غير أن / لكن","however","[ˈalɐˌdɪŋs]",
          "Das Essen war gut, allerdings etwas teuer.",
          "الطعام كان جيداً، غير أنه كان باهظاً بعض الشيء.","The food was good, however a bit expensive.",
          "balance scales comparison two sides","اكتب جملة بـ 'allerdings' عن شيء له جانبان."),
    _card("schließlich","—","-","B1","📝 Grammatik","في النهاية","finally / after all","[ˈʃliːslɪç]",
          "Schließlich haben wir das Ziel erreicht.",
          "في النهاية بلغنا الهدف.","Finally, we reached the goal.",
          "finish line success achievement celebration","اكتب جملة عن هدف حققته في النهاية."),
    _card("Uhr","die","Uhren","A1","⏰ Zeit","ساعة (وقت)","o'clock / clock","[uːɐ]",
          "Es ist jetzt zehn Uhr morgens.",
          "الساعة الآن العاشرة صباحاً.","It is now ten o'clock in the morning.",
          "clock wall time analog","الساعة الآن كم؟ اكتبها بالألمانية."),
    _card("Minute","die","Minuten","A1","⏰ Zeit","دقيقة","minute","[mɪˈnuːtə]",
          "In dreißig Minuten beginnt das Konzert.",
          "بعد ثلاثين دقيقة يبدأ الحفل.","The concert starts in thirty minutes.",
          "timer countdown minutes stopwatch","كم دقيقة تتعلم الألمانية يومياً؟"),
    _card("natürlich","—","-","A2","📐 Adjektive","بالطبع","of course / natural","[naˈtyːʁlɪç]",
          "Natürlich helfe ich dir gerne!",
          "بالطبع يسعدني مساعدتك!","Of course, I'm happy to help you!",
          "nature natural landscape forest","استخدم 'natürlich' في جملة."),
    _card("möglich","—","-","A2","📐 Adjektive","ممكن","possible","[ˈmøːklɪç]",
          "Ist es möglich, Deutsch in 90 Tagen zu lernen?",
          "هل من الممكن تعلم الألمانية في 90 يوماً؟","Is it possible to learn German in 90 days?",
          "possible impossible challenge goal","ما الذي تعتقد أنه ممكن في تعلم الألمانية؟"),
    _card("Verständnis","das","-","B1","💭 Gedanken","فهم / تفهم","understanding","[fɛʁˈʃtɛntnɪs]",
          "Ohne gegenseitiges Verständnis funktioniert keine Freundschaft.",
          "بدون تفاهم متبادل لا تنجح أي صداقة.","Without mutual understanding, no friendship works.",
          "understanding empathy communication people","كيف يساعدك الألمانية على فهم الثقافة الألمانية؟"),
    _card("Zusammenarbeit","die","-","B1","👥 Soziales","تعاون","cooperation / teamwork","[tsʊˈzamənˌaʁbaɪt]",
          "Gute Zusammenarbeit ist der Schlüssel zum Erfolg.",
          "التعاون الجيد هو مفتاح النجاح.","Good cooperation is the key to success.",
          "teamwork collaboration group people","صف موقفاً تعاونت فيه مع شخص آخر."),
]

# ── Dictionary helpers ────────────────────────────────────────────────
def get_dict_by_level(level: str) -> list:
    return [w for w in DICTIONARY if w["level"] == level]

def get_dict_by_category(category: str) -> list:
    return [w for w in DICTIONARY if w["category"] == category]

def search_dictionary(query: str) -> list:
    q = query.lower().strip()
    return [w for w in DICTIONARY if q in w["word"].lower() or q in w["en"].lower() or q in w["ar"]]

def get_all_categories() -> list:
    seen, cats = set(), []
    for w in DICTIONARY:
        if w["category"] not in seen:
            seen.add(w["category"]); cats.append(w["category"])
    return cats

def get_random_words(n: int = 10, level: str = None) -> list:
    import random
    pool = get_dict_by_level(level) if level else DICTIONARY
    return random.sample(pool, min(n, len(pool)))

def render_audio_html(word: str, audio_url: str) -> str:
    aid = f"aud_{word.replace(' ','_').replace('/','')}"
    return (f'<audio id="{aid}" src="{audio_url}" preload="none"></audio>'
            f'<button class="dict-audio-btn" onclick="document.getElementById(\'{aid}\').play()">'
            f'🔊 استمع &nbsp;·&nbsp; Listen</button>')

def render_dict_card(entry: dict, lang: str = "ar") -> str:
    g   = f"{entry['gender']} " if entry.get("gender") and entry["gender"] != "—" else ""
    pl  = f" · Pl: {entry['plural']}" if entry.get("plural") and entry["plural"] not in ["-","None","—"] else ""
    aud = render_audio_html(entry["word"], entry["audio_url"])
    return f"""<div class="dict-card">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
    <div>
      <div class="dict-word">{g}{entry['word']}</div>
      <div class="dict-phonetic">{entry.get('ipa','')} {pl} · <span style="color:#f5c518">{entry['level']}</span> · {entry['category']}</div>
    </div>
    <div>{aud}</div>
  </div>
  <div class="dict-translations">
    <span class="dict-trans-ar">🇪🇬 {entry['ar']}</span>
    <span class="dict-trans-en">🇬🇧 {entry['en']}</span>
  </div>
  <div class="dict-example">
    <div class="dict-example-de">💬 {entry['example_de']}</div>
    <div class="dict-example-ar">↳ {entry['example_ar']}</div>
    <div class="dict-example-en">↳ {entry['example_en']}</div>
  </div>
  <div class="input-box">
    <div style="font-size:.75rem;color:#3b82f6;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">📥 {t('dict_input', lang)}</div>
    <div style="font-size:.86rem;color:#aaa;">🔍 Search images: <em>{entry.get('input_image_keyword','—')}</em></div>
  </div>
  <div class="output-box">
    <div style="font-size:.75rem;color:#22c55e;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">📤 {t('dict_output', lang)}</div>
    <div style="font-size:.86rem;color:#aaa;direction:rtl;">✏️ {entry.get('output_prompt_ar','—')}</div>
  </div>
</div>"""


# ────────────────────────────────────────────────────────────────────
#  8. PHASES, XP, LEVELS, BADGES, MANTRAS  (unchanged from v2)
# ────────────────────────────────────────────────────────────────────
PHASES = [
    {"name":"Foundation","emoji":"🏗️","days":list(range(1,31)), "goal":"Master the alphabet, phonetics, numbers, greetings, and basic grammar.","cefr":"Pre-A1 → A1","color":"#f5c518"},
    {"name":"Construction","emoji":"🧱","days":list(range(31,61)),"goal":"Build sentences, verb conjugation, and grow vocabulary to 500+ words.","cefr":"A1 → A2","color":"#cc0000"},
    {"name":"Activation","emoji":"⚡","days":list(range(61,91)), "goal":"Read, listen, write, and speak in real German contexts.","cefr":"A2 → B1","color":"#22c55e"},
]
PHASE_MAP = {}
for _ph in PHASES:
    for _d in _ph["days"]: PHASE_MAP[_d] = _ph["name"]

XP_RULES = {
    "complete_day":20,"flashcard_correct":3,"flashcard_round":10,"word_match":15,
    "sentence_scramble":20,"grammar_exercise":5,"submit_writing":8,"perfect_day":30,
    "streak_7":50,"streak_30":150,"streak_90":500,"complete_phase_1":100,
    "complete_phase_2":200,"complete_phase_3":400,"first_login":10,"save_word":2,
}

LEVELS = [
    (0,"Anfänger","Beginner"),(100,"Lernender","Learner"),(300,"Entdecker","Explorer"),
    (600,"Schüler","Student"),(1000,"Fortgeschritten","Advanced"),(1500,"Kenner","Connoisseur"),
    (2500,"Experte","Expert"),(4000,"Meister","Master"),(6000,"Großmeister","Grandmaster"),
]
def get_level(xp: int) -> dict:
    info = LEVELS[0]
    for thr, de, en in LEVELS:
        if xp >= thr: info = (thr, de, en)
    t, de, en = info
    idx = next((i for i,(th,_,__) in enumerate(LEVELS) if th == t), len(LEVELS)-1)
    nt  = LEVELS[idx+1][0] if idx+1 < len(LEVELS) else t
    return {"name_de":de,"name_en":en,"threshold":t,"next_xp":nt,"progress":min((xp-t)/max(nt-t,1),1.0),"xp":xp}

BADGES = [
    {"id":"streak_3",  "emoji":"🔥",   "name":"Erste Flamme",   "desc":"3-day streak",        "condition":lambda u:u.get("streak",0)>=3},
    {"id":"streak_7",  "emoji":"🔥🔥", "name":"Wochenheld",     "desc":"7-day streak",        "condition":lambda u:u.get("streak",0)>=7},
    {"id":"streak_30", "emoji":"💎",   "name":"Eisenwille",     "desc":"30-day streak",       "condition":lambda u:u.get("streak",0)>=30},
    {"id":"streak_90", "emoji":"👑",   "name":"Legende",        "desc":"90-day streak",       "condition":lambda u:u.get("streak",0)>=90},
    {"id":"day_1",     "emoji":"🌱",   "name":"Erster Schritt", "desc":"Complete Day 1",      "condition":lambda u:u.get("days_done",0)>=1},
    {"id":"day_7",     "emoji":"📅",   "name":"Eine Woche",     "desc":"Complete 7 days",     "condition":lambda u:u.get("days_done",0)>=7},
    {"id":"day_30",    "emoji":"🏗️",   "name":"Fundament",      "desc":"Complete Phase 1",    "condition":lambda u:u.get("days_done",0)>=30},
    {"id":"day_60",    "emoji":"🧱",   "name":"Konstrukteur",   "desc":"Complete Phase 2",    "condition":lambda u:u.get("days_done",0)>=60},
    {"id":"day_90",    "emoji":"🏆",   "name":"Camp-Absolvent", "desc":"Complete all 90 days","condition":lambda u:u.get("days_done",0)>=90},
    {"id":"xp_100",    "emoji":"⭐",   "name":"Fleißig",        "desc":"Earn 100 XP",         "condition":lambda u:u.get("xp",0)>=100},
    {"id":"xp_500",    "emoji":"🌟",   "name":"Strebsam",       "desc":"Earn 500 XP",         "condition":lambda u:u.get("xp",0)>=500},
    {"id":"xp_2000",   "emoji":"💫",   "name":"Hochleistung",   "desc":"Earn 2000 XP",        "condition":lambda u:u.get("xp",0)>=2000},
    {"id":"gamer",     "emoji":"🎮",   "name":"Spieler",        "desc":"Play 5 mini-games",   "condition":lambda u:u.get("games_played",0)>=5},
    {"id":"champion",  "emoji":"🥊",   "name":"Champion",       "desc":"Win 20 mini-games",   "condition":lambda u:u.get("games_won",0)>=20},
    {"id":"writer",    "emoji":"✍️",   "name":"Schreiber",      "desc":"Submit 5 writings",   "condition":lambda u:u.get("submissions",0)>=5},
    {"id":"vocab_50",  "emoji":"📖",   "name":"Vokabelmeister", "desc":"Save 50 words",        "condition":lambda u:u.get("saved_words",0)>=50},
]

MANTRAS = [
    ('"Sprache ist nicht nur Kommunikation — sie ist Identität." 🇩🇪',"Language is not just communication — it is identity."),
    ('"Every German word you learn is a door to a new world."',""),
    ('"Fehler machen ist menschlich. Aufhören ist optional."',"Making mistakes is human. Quitting is optional."),
    ('"Du schaffst das! One day at a time, one word at a time."',""),
    ('"Übung macht den Meister."',"Practice makes perfect."),
    ('"Der Weg ist das Ziel." — Konfuzius',"The journey is the destination."),
    ('"Ohne Fleiß kein Preis."',"No pain, no gain."),
    ('"Wer nicht wagt, der nicht gewinnt."',"Nothing ventured, nothing gained."),
    ('"Ein Schritt nach dem anderen führt zum Ziel."',"One step at a time leads to the goal."),
    ('"Repetition is the mother of mastery. Wiederholen = Meistern."',""),
]

GRAMMAR_TOPICS = {
    "Foundation":["Der/Die/Das — Articles","sein (to be)","haben (to have)","Personal Pronouns","Nominative Case","Present Tense (Präsens)","Yes/No Questions","Numbers 1–100","Time expressions","Negation — kein/nicht"],
    "Construction":["Accusative Case","Dative Case","Modal Verbs","Separable Verbs","Adjective Endings","Prepositions + Accusative","Prepositions + Dative","Two-way Prepositions","Perfect Tense (Perfekt)","Word Order TMP"],
    "Activation":["Subordinate Clauses — weil/dass/wenn","Relative Clauses","Präteritum (narrative past)","Future Tense (Futur I)","Konjunktiv II","Passive Voice","Comparative & Superlative","Genitive Case","Reflexive Verbs","Infinitive Constructions um…zu"],
}

PHONETICS = [
    {"sym":"r",    "name":"Das R",   "ipa":"[ʁ]",      "desc":"Guttural — gargle softly",         "yt":"oRpSJXMJUDg","example_words":["rot","reisen","Bruder","Frühling"]},
    {"sym":"ch",   "name":"Das CH",  "ipa":"[ç]/[x]",  "desc":"ich-Laut vs ach-Laut",             "yt":"pN3Aqs9BGLM","example_words":["ich","acht","durch","Bücher"]},
    {"sym":"ä",    "name":"Das Ä",   "ipa":"[ɛ]",      "desc":"Like 'air' but shorter",           "yt":"XbiBS5YIQB0","example_words":["Mädchen","Käse","wählen","Äpfel"]},
    {"sym":"ö",    "name":"Das Ö",   "ipa":"[ø]",      "desc":"Round lips, say 'e'",              "yt":"XbiBS5YIQB0","example_words":["schön","hören","Öl","möchten"]},
    {"sym":"ü",    "name":"Das Ü",   "ipa":"[y]",      "desc":"Round lips, say 'i'",              "yt":"XbiBS5YIQB0","example_words":["über","grün","müde","fühlen"]},
    {"sym":"ß",    "name":"Das ß",   "ipa":"[sː]",     "desc":"Sharp SS — never word-start",      "yt":"oRpSJXMJUDg","example_words":["Straße","heiß","Fuß","groß"]},
    {"sym":"z",    "name":"Das Z",   "ipa":"[ts]",     "desc":"Always 'ts' — never English z",    "yt":"oRpSJXMJUDg","example_words":["Zeit","zehn","Zug","bezahlen"]},
    {"sym":"w",    "name":"Das W",   "ipa":"[v]",      "desc":"Pronounced like English 'v'",      "yt":"oRpSJXMJUDg","example_words":["Wasser","wohnen","Welt","schwimmen"]},
    {"sym":"v",    "name":"Das V",   "ipa":"[f]",      "desc":"Usually like 'f'",                 "yt":"oRpSJXMJUDg","example_words":["Vater","vier","voll","Vogel"]},
    {"sym":"sp/st","name":"SP/ST",   "ipa":"[ʃp/ʃt]",  "desc":"Word start: 'shp' and 'sht'",     "yt":"oRpSJXMJUDg","example_words":["sprechen","Stadt","Stein","spät"]},
]

MINIMAL_PAIRS = [
    ("bitten","bieten","to ask / to offer"),("Hölle","Höhle","hell / cave"),
    ("Bach","Buch","stream / book"),("fahren","fähren","to drive / ferries"),
    ("lesen","essen","to read / to eat"),("suchen","kochen","to search / to cook"),
    ("kennen","können","to know / can"),("liegen","legen","to lie / to place"),
    ("sehen","stehen","to see / to stand"),("fallen","füllen","to fall / to fill"),
]

CULTURAL_DROPS = [
    {"week":1, "title":"Pünktlichkeit 🕐","body":"'Pünktlichkeit ist die Höflichkeit der Könige.' 5 min early = respectful. 5 min late = apologize."},
    {"week":2, "title":"Kaffee & Kuchen ☕","body":"Sunday 3–4pm family coffee and homemade cake — less about food, more about slowing down."},
    {"week":3, "title":"Recycling ♻️","body":"Germany's Pfand bottle deposit makes sustainability personal. Green Grüner Punkt = recyclable."},
    {"week":4, "title":"Brot & Backen 🥖","body":"3,200+ bread varieties. Homesickness (Heimweh) often starts with missing Brot."},
    {"week":5, "title":"Feierabend 🍺","body":"After Feierabend (end of workday) — no emails, no calls. Work simply doesn't exist."},
    {"week":6, "title":"Ordnung 📋","body":"'Ordnung muss sein.' 5+ trash categories, Anmeldung address registration, official Sunday quiet hours (Ruhezeit)."},
    {"week":7, "title":"Wandern 🏔️","body":"Hiking is a national hobby — complete with proper gear, documented trails, and Wanderlieder (hiking songs)."},
    {"week":8, "title":"Direkte Kommunikation 🗣️","body":"German directness = respect. 'Das stimmt nicht' (That's wrong) is normal in meetings, not rude."},
    {"week":9, "title":"Apotheke 💊","body":"The local pharmacy is a trusted institution — pharmacists spend time consulting, not just dispensing."},
    {"week":10,"title":"Weihnachten 🎄","body":"Christmas is a full Advent season — 4 Sundays of Adventskalender, Weihnachtsmärkte, Glühwein, Lebkuchen."},
    {"week":11,"title":"Die Deutsche Bahn 🚂","body":"Train delays (Verspätung) are a shared cultural bond — strangers unite on platforms."},
    {"week":12,"title":"Fußball & Verein 🏆","body":"Every town has a Verein (club) — football, singing, chess. Often older than the town hall."},
]

RESOURCES = [
    {"cat":"📺 Video","name":"Nicos Weg (DW) — A1 Series","url":"https://www.dw.com/de/nicos-weg/s-52164","desc":"30-min episodes, perfect for A1"},
    {"cat":"📺 Video","name":"Easy German — Street Interviews","url":"https://www.youtube.com/@EasyGerman","desc":"Authentic German with subtitles"},
    {"cat":"📺 Video","name":"Deutsch für Euch — Grammar Deep Dives","url":"https://www.youtube.com/@DeutschFuerEuch","desc":"Best grammar on YouTube"},
    {"cat":"🃏 Anki","name":"AnkiWeb — Sync Decks","url":"https://ankiweb.net","desc":"Free cross-device sync"},
    {"cat":"🃏 Anki","name":"German Core 2k/6k Deck","url":"https://ankiweb.net/shared/info/1558798271","desc":"Most common 2000 words"},
    {"cat":"🔊 Audio","name":"YouGlish German","url":"https://youglish.com/german","desc":"Any word spoken by native speakers"},
    {"cat":"🔊 Audio","name":"Slow German Podcast","url":"https://slowgerman.com","desc":"Designed for learners"},
    {"cat":"🔊 Audio","name":"Forvo — Pronunciation DB","url":"https://forvo.com/languages/de/","desc":"Native speaker recordings"},
    {"cat":"📖 Read","name":"DW Learn German Articles","url":"https://www.dw.com/en/learn-german/s-2053","desc":"Current events in simple German"},
    {"cat":"📖 Read","name":"Nachrichtenleicht — Easy News","url":"https://www.nachrichtenleicht.de","desc":"Weekly news in simple German"},
    {"cat":"🛠️ Tools","name":"dict.cc — Best Dictionary","url":"https://www.dict.cc","desc":"Comprehensive with examples"},
    {"cat":"🛠️ Tools","name":"Reverso Context","url":"https://context.reverso.net/translation/german-english/","desc":"Words in real sentences"},
    {"cat":"🛠️ Tools","name":"LanguageTool — Grammar Checker","url":"https://languagetool.org","desc":"Free AI grammar checker"},
    {"cat":"📚 Books","name":"Schritte Plus Neu A1","url":"https://www.amazon.com/s?k=Schritte+Plus+Neu+A1","desc":"Most-used A1 textbook"},
    {"cat":"📚 Books","name":"Hammer's German Grammar","url":"https://www.amazon.com/s?k=Hammers+German+Grammar","desc":"Definitive grammar reference"},
]
