# ═══════════════════════════════════════════════
#  config.py  —  German Mastery Camp
#  Central configuration for the entire platform
# ═══════════════════════════════════════════════

import streamlit as st

# ── App Identity ────────────────────────────────
APP_NAME        = "German Mastery Camp"
APP_TAGLINE     = "Learning is living — not just memorizing."
APP_VERSION     = "2.0.0"
APP_EMOJI       = "🇩🇪"
CAMP_DURATION   = 90   # days

# ── API KEYS ─────────────────────────────────────
# temporary hard‑coded key for development; in production move to secrets
GROQ_API_KEY    = "gsk_NE1SSBNN0JDcu3CHywFmWGdy3FY7quioGA7UCAe5FHKudZRZ0CQ"


# ── Colors ──────────────────────────────────────
COLORS = {
    "black":   "#0d0d0d",
    "red":     "#cc0000",
    "gold":    "#f5c518",
    "gold2":   "#d4a017",
    "white":   "#f8f5ef",
    "card":    "#1a1a1a",
    "border":  "#2e2e2e",
    "muted":   "#777",
    "success": "#22c55e",
    "info":    "#3b82f6",
}

# ── Phases ──────────────────────────────────────
PHASES = [
    {
        "name":        "Foundation",
        "emoji":       "🏗️",
        "days":        list(range(1,  31)),
        "goal":        "Master the alphabet, phonetics, numbers, greetings, and basic grammar.",
        "cefr":        "Pre-A1 → A1",
        "color":       "#f5c518",
    },
    {
        "name":        "Construction",
        "emoji":       "🧱",
        "days":        list(range(31, 61)),
        "goal":        "Build sentences, learn verb conjugation, and grow your vocabulary to 500+ words.",
        "cefr":        "A1 → A2",
        "color":       "#cc0000",
    },
    {
        "name":        "Activation",
        "emoji":       "⚡",
        "days":        list(range(61, 91)),
        "goal":        "Read, listen, write, and speak in real German contexts.",
        "cefr":        "A2 → B1",
        "color":       "#22c55e",
    },
]

PHASE_MAP = {}
for ph in PHASES:
    for d in ph["days"]:
        PHASE_MAP[d] = ph["name"]

# ── XP System ───────────────────────────────────
XP_RULES = {
    "complete_day":          20,
    "flashcard_correct":     3,
    "flashcard_round":       10,
    "word_match":            15,
    "sentence_scramble":     20,
    "grammar_exercise":      5,
    "submit_writing":        8,
    "perfect_day":           30,   # all 4 tasks + a game
    "streak_7":              50,
    "streak_30":             150,
    "streak_90":             500,
    "complete_phase_1":      100,
    "complete_phase_2":      200,
    "complete_phase_3":      400,
    "first_login":           10,
}

# XP thresholds → Level names
LEVELS = [
    (0,    "Anfänger",       "Beginner"),
    (100,  "Lernender",      "Learner"),
    (300,  "Entdecker",      "Explorer"),
    (600,  "Schüler",        "Student"),
    (1000, "Fortgeschritten","Advanced"),
    (1500, "Kenner",         "Connoisseur"),
    (2500, "Experte",        "Expert"),
    (4000, "Meister",        "Master"),
    (6000, "Großmeister",    "Grandmaster"),
]

def get_level(xp: int) -> dict:
    level_info = LEVELS[0]
    for threshold, de, en in LEVELS:
        if xp >= threshold:
            level_info = (threshold, de, en)
    t, de, en = level_info
    # Find next level
    idx = next((i for i,(th,_,__) in enumerate(LEVELS) if th == t), len(LEVELS)-1)
    next_th = LEVELS[idx+1][0] if idx+1 < len(LEVELS) else t
    progress = (xp - t) / max(next_th - t, 1)
    return {
        "name_de":   de,
        "name_en":   en,
        "threshold": t,
        "next_xp":   next_th,
        "progress":  min(progress, 1.0),
        "xp":        xp,
    }

# ── Badges / Achievements ────────────────────────
BADGES = [
    # Streak badges
    {"id": "streak_3",    "emoji": "🔥",  "name": "Erste Flamme",    "desc": "3-day streak",         "condition": lambda u: u.get("streak",0) >= 3},
    {"id": "streak_7",    "emoji": "🔥🔥", "name": "Wochenheld",      "desc": "7-day streak",         "condition": lambda u: u.get("streak",0) >= 7},
    {"id": "streak_30",   "emoji": "💎",  "name": "Eisenwille",      "desc": "30-day streak",        "condition": lambda u: u.get("streak",0) >= 30},
    {"id": "streak_90",   "emoji": "👑",  "name": "Legende",         "desc": "90-day streak",        "condition": lambda u: u.get("streak",0) >= 90},
    # Day completion badges
    {"id": "day_1",       "emoji": "🌱",  "name": "Erster Schritt",  "desc": "Complete Day 1",       "condition": lambda u: u.get("days_done",0) >= 1},
    {"id": "day_7",       "emoji": "📅",  "name": "Eine Woche",      "desc": "Complete 7 days",      "condition": lambda u: u.get("days_done",0) >= 7},
    {"id": "day_30",      "emoji": "🏗️",  "name": "Fundament",       "desc": "Complete Phase 1",     "condition": lambda u: u.get("days_done",0) >= 30},
    {"id": "day_60",      "emoji": "🧱",  "name": "Konstrukteur",    "desc": "Complete Phase 2",     "condition": lambda u: u.get("days_done",0) >= 60},
    {"id": "day_90",      "emoji": "🏆",  "name": "Camp-Absolvant",  "desc": "Complete all 90 days", "condition": lambda u: u.get("days_done",0) >= 90},
    # XP badges
    {"id": "xp_100",      "emoji": "⭐",  "name": "Fleißig",         "desc": "Earn 100 XP",          "condition": lambda u: u.get("xp",0) >= 100},
    {"id": "xp_500",      "emoji": "🌟",  "name": "Strebsam",        "desc": "Earn 500 XP",          "condition": lambda u: u.get("xp",0) >= 500},
    {"id": "xp_2000",     "emoji": "💫",  "name": "Hochleistung",    "desc": "Earn 2000 XP",         "condition": lambda u: u.get("xp",0) >= 2000},
    # Game badges
    {"id": "gamer",       "emoji": "🎮",  "name": "Spieler",         "desc": "Play 5 mini-games",    "condition": lambda u: u.get("games_played",0) >= 5},
    {"id": "champion",    "emoji": "🥊",  "name": "Champion",        "desc": "Win 20 mini-games",    "condition": lambda u: u.get("games_won",0) >= 20},
    # Writing badges
    {"id": "writer",      "emoji": "✍️",  "name": "Schreiber",       "desc": "Submit 5 writings",    "condition": lambda u: u.get("submissions",0) >= 5},
    {"id": "author",      "emoji": "📝",  "name": "Autor",           "desc": "Submit 20 writings",   "condition": lambda u: u.get("submissions",0) >= 20},
]

def check_new_badges(user_stats: dict, existing_badge_ids: list) -> list:
    """Return list of newly earned badge dicts."""
    new = []
    for badge in BADGES:
        if badge["id"] not in existing_badge_ids:
            try:
                if badge["condition"](user_stats):
                    new.append(badge)
            except Exception:
                pass
    return new

# ── Mantras ──────────────────────────────────────
MANTRAS = [
    ('"Sprache ist nicht nur Kommunikation — sie ist Identität." 🇩🇪',
     "Language is not just communication — it is identity."),
    ('"Every German word you learn is a door to a new world."', ""),
    ('"Fehler machen ist menschlich. Aufhören ist optional."',
     "Making mistakes is human. Quitting is optional."),
    ('"Du schaffst das! One day at a time, one word at a time."', ""),
    ('"Repetition is the mother of mastery. Wiederholen = Meistern."', ""),
    ('"Ein Schritt nach dem anderen führt zum Ziel."',
     "One step at a time leads to the goal."),
    ('"Wer nicht wagt, der nicht gewinnt."',
     "Nothing ventured, nothing gained."),
    ('"Übung macht den Meister."',
     "Practice makes perfect (literally: practice makes the master)."),
    ('"Der Weg ist das Ziel." — Konfuzius',
     "The journey is the destination."),
    ('"Ohne Fleiß kein Preis."',
     "No pain, no gain."),
]

# ── TRANSLATIONS / I18N ─────────────────────────────
LANGUAGES = ["en", "ar"]
TRANSLATIONS = {
    "en": {
        "sign_in": "Sign In",
        "password": "Password",
        "email": "Email",
        "create_account": "Create Account",
        "admin_login": "Admin Login",
        "welcome": "Welcome, {name}!",
        "home_subtitle": "*Learning is living — not just memorizing.*",
        "daily_mission": "Daily Mission",
        "complete_day": "Complete Day {day} — Earn 20 XP",
        "locked":"Locked", "available":"Available","completed":"Completed",
        "search_topic": "Search topic",
        "play": "Play →",
        "send": "Send →",
        "clear_chat": "Clear Chat",
        "grammar_fixer": "AI Grammar Fixer",
        "chat_placeholder": "Ask Klaus anything about German…",
        "logout": "Sign Out",
        "progress": "Progress",
        "xp": "XP",
        "streak": "Streak",
        "days": "days",
        "home_title": "🇩🇪 Willkommen, {name}!",
        "roadmap_title": "🗺️ Learning Roadmap",
        "output_title": "🖼️ Output Comprehension",
        "dictionary_title": "📖 Smart Dictionary",
        "admin_panel": "⚙️ Admin Panel",
    },
    "ar": {
        "sign_in": "تسجيل الدخول",
        "password": "كلمة المرور",
        "email": "البريد الإلكتروني",
        "create_account": "إنشاء حساب",
        "admin_login": "تسجيل دخول المسؤول",
        "welcome": "أهلاً بك، {name}!",
        "home_subtitle": "*التعلم هو الحياة — ليس مجرد حفظ.*",
        "daily_mission": "مهمة اليوم",
        "complete_day": "أكمل اليوم {day} — احصل على 20 نقاط XP",
        "locked":"مقفلة", "available":"متاحة","completed":"مكتملة",
        "search_topic": "ابحث عن موضوع",
        "play": "العب →",
        "send": "إرسال →",
        "clear_chat": "مسح الدردشة",
        "grammar_fixer": "مدقق القواعد بواسطة الذكاء الاصطناعي",
        "chat_placeholder": "اسأل كلاوس أي شيء عن الألمانية...",
        "logout": "تسجيل الخروج",
        "progress": "التقدم",
        "xp": "XP",
        "streak": "سلسلة",
        "days": "أيام",
        "home_title": "🇩🇪 مرحباً، {name}!",
        "roadmap_title": "🗺️ خريطة التعلم",
        "output_title": "🖼️ فهم المخرجات",
        "dictionary_title": "📖 القاموس الذكي",
        "admin_panel": "⚙️ لوحة الإدارة",
    },
}

def tr(key: str, **kwargs) -> str:
    """Return translated string for current language."""
    lang = kwargs.pop('lang', None)
    if lang is None:
        lang = st.session_state.get('lang', 'en')
    text = TRANSLATIONS.get(lang, {}).get(key, key)
    try:
        return text.format(**kwargs)
    except Exception:
        return text


# ── Grammar Topics by Phase ──────────────────────
GRAMMAR_TOPICS = {
    "Foundation": [
        "Der / Die / Das — German Articles",
        "Verb: sein (to be) — ich bin, du bist...",
        "Verb: haben (to have) — ich habe...",
        "Personal Pronouns — ich, du, er, sie, wir...",
        "Nominative Case — Subject of the sentence",
        "Simple Present Tense (Präsens)",
        "Yes/No Questions",
        "Numbers 1–100",
        "Time expressions — heute, morgen, gestern",
        "Negation — kein / nicht",
    ],
    "Construction": [
        "Accusative Case — Direct object",
        "Dative Case — Indirect object",
        "Modal Verbs — können, müssen, wollen, dürfen",
        "Separable Verbs — aufmachen, anrufen...",
        "Adjective Endings",
        "Prepositions with Accusative",
        "Prepositions with Dative",
        "Two-way Prepositions",
        "Perfect Tense (Perfekt) — haben/sein + Partizip",
        "Word Order — Time-Manner-Place (TMP)",
    ],
    "Activation": [
        "Subordinate Clauses — weil, dass, wenn, obwohl",
        "Relative Clauses",
        "Simple Past (Präteritum) — narrative tense",
        "Future Tense (Futur I)",
        "Konjunktiv II — würde, wäre, hätte",
        "Passive Voice",
        "Comparative & Superlative",
        "Genitive Case",
        "Reflexive Verbs",
        "Infinitive Constructions — um...zu",
    ],
}

# ── Phonetics ────────────────────────────────────
PHONETICS = [
    {"sym":"r",  "name":"Das R",  "ipa":"[ʁ]", "desc":"Guttural — like gargling softly in throat",  "yt":"oRpSJXMJUDg", "example_words":["rot","reisen","Bruder","Frühling"]},
    {"sym":"ch", "name":"Das CH", "ipa":"[ç]/[x]","desc":"Soft 'ich-Laut' vs hard 'ach-Laut'",     "yt":"pN3Aqs9BGLM", "example_words":["ich","acht","durch","Bücher"]},
    {"sym":"ä",  "name":"Das Ä",  "ipa":"[ɛ]", "desc":"Like English 'air' but shorter & cleaner",  "yt":"XbiBS5YIQB0", "example_words":["Mädchen","Käse","wählen","Äpfel"]},
    {"sym":"ö",  "name":"Das Ö",  "ipa":"[ø]", "desc":"Round your lips then try to say 'e'",       "yt":"XbiBS5YIQB0", "example_words":["schön","hören","Öl","möchten"]},
    {"sym":"ü",  "name":"Das Ü",  "ipa":"[y]", "desc":"Round your lips then try to say 'i'",       "yt":"XbiBS5YIQB0", "example_words":["über","grün","müde","fühlen"]},
    {"sym":"ß",  "name":"Das ß",  "ipa":"[sː]","desc":"Sharp SS — never at start of word",         "yt":"oRpSJXMJUDg", "example_words":["Straße","heiß","Fuß","groß"]},
    {"sym":"z",  "name":"Das Z",  "ipa":"[ts]","desc":"Always 'ts' sound — never English 'z'",     "yt":"oRpSJXMJUDg", "example_words":["Zeit","zehn","Zug","bezahlen"]},
    {"sym":"w",  "name":"Das W",  "ipa":"[v]", "desc":"Pronounced like English 'v'",               "yt":"oRpSJXMJUDg", "example_words":["Wasser","wohnen","Welt","schwimmen"]},
    {"sym":"v",  "name":"Das V",  "ipa":"[f]", "desc":"Usually pronounced like 'f'",               "yt":"oRpSJXMJUDg", "example_words":["Vater","vier","voll","Vogel"]},
    {"sym":"sp/st","name":"SP/ST","ipa":"[ʃp/ʃt]","desc":"At word start: 'shp' and 'sht'",        "yt":"oRpSJXMJUDg", "example_words":["sprechen","Stadt","Stein","spät"]},
]

MINIMAL_PAIRS = [
    ("bitten","bieten","to ask / to offer"),
    ("Hölle","Höhle","hell / cave"),
    ("Bach","Buch","stream / book"),
    ("fahren","fähren","to drive / ferries"),
    ("lesen","essen","to read / to eat"),
    ("suchen","kochen","to search / to cook"),
    ("kennen","können","to know (person) / can"),
    ("liegen","legen","to lie down / to place"),
    ("sehen","stehen","to see / to stand"),
    ("fallen","füllen","to fall / to fill"),
]

# ── Cultural Drops ───────────────────────────────
CULTURAL_DROPS = [
    {"week":1,  "title":"Pünktlichkeit 🕐",     "body":"Germans treat punctuality as a form of respect. Arriving 5 minutes early is normal — 5 minutes late requires an apology. The phrase 'Pünktlichkeit ist die Höflichkeit der Könige' (Punctuality is the politeness of kings) lives in daily culture."},
    {"week":2,  "title":"Kaffee & Kuchen ☕",   "body":"Sunday afternoon Kaffee und Kuchen is sacred. Families gather around 3–4pm, drink filter coffee, and eat homemade cakes. It's less about the food and more about slowing down together."},
    {"week":3,  "title":"Recycling ♻️",         "body":"Germany's Pfand system (bottle deposits) means every plastic bottle and can has monetary value. People return them religiously. The green Grüner Punkt symbol on packaging signals it belongs to a recycling system."},
    {"week":4,  "title":"Brot & Backen 🥖",     "body":"Germany has 3,200+ registered bread varieties — more than any other country. Bread is emotional. Expats abroad often cite missing German bread (Brot) as their strongest Heimweh (homesickness)."},
    {"week":5,  "title":"Feierabend 🍺",        "body":"Feierabend (literally 'celebration evening') is the sacred end of the workday. After Feierabend, work doesn't exist. No emails, no calls. It's a cultural commitment to the separation of work and life."},
    {"week":6,  "title":"Ordnung 📋",           "body":"'Ordnung muss sein' (There must be order) is a national philosophy. Germans separate trash into 5+ categories, register their address with local authorities (Anmeldung), and have official rules for Sunday quiet time (Ruhezeit)."},
    {"week":7,  "title":"Wandern 🏔️",           "body":"Hiking (Wandern) is a national hobby, not just exercise. Germans of all ages hike — with proper gear, documented trails, and traditional Wanderlieder (hiking songs). Many friendships and business deals begin on a trail."},
    {"week":8,  "title":"Direkte Kommunikation 🗣️","body":"Germans are famously direct — not to be rude, but because they consider clarity respectful. 'Das stimmt nicht' (That's wrong) is a normal response in meetings. This directness can feel harsh to other cultures but builds genuine trust."},
    {"week":9,  "title":"Apotheke & Gesundheit 💊","body":"Germans deeply respect medical expertise. The local Apotheke (pharmacy) is a trusted institution — pharmacists spend extensive time consulting customers. 'Ich gehe zum Arzt' (I'm going to the doctor) requires no justification."},
    {"week":10, "title":"Weihnachten 🎄",        "body":"Christmas isn't a single day — it's a season. Advent begins 4 Sundays before December 24th, with Adventskalender, Adventskränze, and Weihnachtsmärkte (Christmas markets) filling every city with Glühwein and Lebkuchen."},
    {"week":11, "title":"Die Deutsche Bahn 🚂",  "body":"The national railway is simultaneously loved and complained about. Trains are the backbone of German travel, but Verspätung (delay) announcements are a shared cultural experience that bonds strangers on platforms."},
    {"week":12, "title":"Fußball & Verein 🏆",  "body":"Every German town, no matter how small, has a Verein (club) — for football, singing, chess, or gardening. Club membership is how communities form. The local Fußballverein (football club) is often older than the town hall."},
]

# ── Resources ────────────────────────────────────
RESOURCES = [
    {"cat":"📺 Video",  "name":"Nicos Weg (DW) — A1 Series",          "url":"https://www.dw.com/de/nicos-weg/s-52164",    "desc":"30-min episodes, perfect for A1"},
    {"cat":"📺 Video",  "name":"Easy German — Street Interviews",       "url":"https://www.youtube.com/@EasyGerman",        "desc":"Authentic German with subtitles"},
    {"cat":"📺 Video",  "name":"Deutsch für Euch — Grammar Deep Dives", "url":"https://www.youtube.com/@DeutschFuerEuch",   "desc":"Best grammar explanations on YouTube"},
    {"cat":"📺 Video",  "name":"Nico's Weg B1 — DW Advanced",          "url":"https://www.dw.com/de/deutsch-lernen/s-1420","desc":"Follow-up series for B1 level"},
    {"cat":"🃏 Anki",   "name":"AnkiWeb — Sync Your Decks",             "url":"https://ankiweb.net",                        "desc":"Free cross-device flashcard sync"},
    {"cat":"🃏 Anki",   "name":"German Core 2k/6k Deck",               "url":"https://ankiweb.net/shared/info/1558798271", "desc":"Most common 2000 German words"},
    {"cat":"🃏 Anki",   "name":"A1–A2 Vocabulary Deck",                "url":"https://ankiweb.net/shared/info/1651401625", "desc":"Curated for beginners"},
    {"cat":"🔊 Audio",  "name":"YouGlish German",                       "url":"https://youglish.com/german",               "desc":"Hear any word from native speakers"},
    {"cat":"🔊 Audio",  "name":"Slow German Podcast",                   "url":"https://slowgerman.com",                    "desc":"Podcast designed for learners"},
    {"cat":"🔊 Audio",  "name":"Forvo — Pronunciation Database",        "url":"https://forvo.com/languages/de/",           "desc":"Native speaker recordings for every word"},
    {"cat":"🔊 Audio",  "name":"Deutsch, warum nicht? (DW Podcast)",    "url":"https://www.dw.com/de/deutsch-warum-nicht/s-2548","desc":"Classic beginner radio series"},
    {"cat":"📖 Read",   "name":"DW Learn German — Articles",            "url":"https://www.dw.com/en/learn-german/s-2053", "desc":"Current events in simple German"},
    {"cat":"📖 Read",   "name":"Nachrichtenleicht — Easy News",         "url":"https://www.nachrichtenleicht.de",          "desc":"Weekly news in simple German"},
    {"cat":"📖 Read",   "name":"Simple German Texts (A1–B1)",           "url":"https://www.deutschakademie.de/online-deutschkurs/blog/en/simple-german-texts/","desc":"Graded reading practice"},
    {"cat":"🛠️ Tools",  "name":"dict.cc — Best German Dictionary",     "url":"https://www.dict.cc",                       "desc":"Comprehensive with usage examples"},
    {"cat":"🛠️ Tools",  "name":"Reverso Context — Words in Sentences", "url":"https://context.reverso.net/translation/german-english/","desc":"See how words are actually used"},
    {"cat":"🛠️ Tools",  "name":"LanguageTool — Grammar Checker",       "url":"https://languagetool.org",                  "desc":"Free AI grammar correction"},
    {"cat":"🛠️ Tools",  "name":"Canoo.net — Deep Grammar Reference",   "url":"http://canoo.net",                          "desc":"Complete German grammar tables"},
    {"cat":"📚 Books",  "name":"Schritte Plus Neu A1 (Textbook)",       "url":"https://www.amazon.com/s?k=Schritte+Plus+Neu+A1","desc":"Most used A1 textbook in Germany"},
    {"cat":"📚 Books",  "name":"Hammer's German Grammar (Reference)",   "url":"https://www.amazon.com/s?k=Hammers+German+Grammar","desc":"The definitive English-language grammar reference"},
]
