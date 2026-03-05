# ═══════════════════════════════════════════════
#  utils.py  —  German Mastery Camp
#  SRS · Badges · Certificate · Analytics · Email
# ═══════════════════════════════════════════════

import datetime
import json
import math
import random
import hashlib
from typing import Optional

# ────────────────────────────────────────────────────────────
#  SPACED REPETITION SYSTEM  (SM-2 Algorithm)
# ────────────────────────────────────────────────────────────
class SRSCard:
    """
    Implements the SM-2 spaced repetition algorithm.
    
    Quality ratings:
        0 = blackout — complete failure
        1 = wrong but remembered after hint
        2 = wrong but easy to recall
        3 = correct but difficult
        4 = correct with hesitation
        5 = perfect recall
    """
    def __init__(self, card_id: str, word_de: str, word_en: str):
        self.id           = card_id
        self.word_de      = word_de
        self.word_en      = word_en
        self.easiness     = 2.5      # E-Factor
        self.interval     = 1        # days until next review
        self.repetitions  = 0        # times reviewed
        self.next_review  = datetime.date.today()
        self.last_quality = None

    def review(self, quality: int) -> int:
        """Process a review. Returns next interval in days."""
        q = max(0, min(5, quality))
        if q < 3:
            self.repetitions = 0
            self.interval    = 1
        else:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.easiness)
            self.repetitions += 1

        self.easiness = max(1.3, self.easiness + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        self.last_quality = q
        self.next_review  = datetime.date.today() + datetime.timedelta(days=self.interval)
        return self.interval

    def is_due(self) -> bool:
        return datetime.date.today() >= self.next_review

    def to_dict(self) -> dict:
        return {
            "id": self.id, "word_de": self.word_de, "word_en": self.word_en,
            "easiness": self.easiness, "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review": self.next_review.isoformat(),
            "last_quality": self.last_quality,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SRSCard":
        c = cls(d["id"], d["word_de"], d["word_en"])
        c.easiness    = d.get("easiness", 2.5)
        c.interval    = d.get("interval", 1)
        c.repetitions = d.get("repetitions", 0)
        c.last_quality = d.get("last_quality")
        nr = d.get("next_review")
        c.next_review = datetime.date.fromisoformat(nr) if nr else datetime.date.today()
        return c


class SRSDeck:
    """Manages a collection of SRS cards."""
    def __init__(self):
        self.cards: dict[str, SRSCard] = {}

    def add_card(self, word_de: str, word_en: str) -> SRSCard:
        cid = hashlib.md5(word_de.encode()).hexdigest()[:8]
        if cid not in self.cards:
            self.cards[cid] = SRSCard(cid, word_de, word_en)
        return self.cards[cid]

    def due_cards(self) -> list[SRSCard]:
        return sorted(
            [c for c in self.cards.values() if c.is_due()],
            key=lambda c: c.next_review
        )

    def new_cards(self, limit: int = 10) -> list[SRSCard]:
        return [c for c in self.cards.values() if c.repetitions == 0][:limit]

    def stats(self) -> dict:
        cards = list(self.cards.values())
        if not cards:
            return {"total": 0, "due": 0, "new": 0, "mature": 0, "retention": 0.0}
        mature = [c for c in cards if c.interval >= 21]
        due    = [c for c in cards if c.is_due()]
        good   = [c for c in cards if c.last_quality and c.last_quality >= 3]
        return {
            "total":     len(cards),
            "due":       len(due),
            "new":       len([c for c in cards if c.repetitions == 0]),
            "mature":    len(mature),
            "retention": len(good) / max(len(cards), 1),
        }

    def to_json(self) -> str:
        return json.dumps({cid: c.to_dict() for cid, c in self.cards.items()})

    @classmethod
    def from_json(cls, raw: str) -> "SRSDeck":
        deck = cls()
        try:
            data = json.loads(raw)
            for cid, d in data.items():
                deck.cards[cid] = SRSCard.from_dict(d)
        except Exception:
            pass
        return deck


# ────────────────────────────────────────────────────────────
#  STREAK HELPERS
# ────────────────────────────────────────────────────────────
def compute_streak(completed_days: set) -> int:
    if not completed_days:
        return 0
    streak, d = 0, max(completed_days)
    while d in completed_days:
        streak += 1
        d -= 1
    return streak

def days_until_level_up(xp: int) -> int:
    """Estimate days to next XP level at 20 XP/day."""
    from config import LEVELS
    for threshold, _, __ in LEVELS:
        if xp < threshold:
            return max(1, math.ceil((threshold - xp) / 20))
    return 0

def weekly_xp_goal(streak: int) -> int:
    """Dynamic weekly XP goal based on current streak."""
    base = 100
    if streak >= 30:  return 300
    if streak >= 14:  return 200
    if streak >= 7:   return 150
    return base


# ────────────────────────────────────────────────────────────
#  BADGE SYSTEM
# ────────────────────────────────────────────────────────────
def evaluate_badges(user_stats: dict) -> list[dict]:
    """
    Returns list of ALL earned badges given user_stats dict.
    
    user_stats keys: xp, streak, days_done, games_played, games_won, submissions
    """
    from config import BADGES
    earned = []
    for badge in BADGES:
        try:
            if badge["condition"](user_stats):
                earned.append({k: v for k, v in badge.items() if k != "condition"})
        except Exception:
            pass
    return earned

def get_new_badges(user_stats: dict, existing_ids: list) -> list[dict]:
    """Returns only NEWLY earned badges not in existing_ids."""
    all_earned = evaluate_badges(user_stats)
    return [b for b in all_earned if b["id"] not in existing_ids]

def build_user_stats(session_state) -> dict:
    """Build stats dict from Streamlit session state for badge evaluation."""
    return {
        "xp":          session_state.get("xp", 0),
        "streak":      compute_streak(session_state.get("completed_days", set())),
        "days_done":   len(session_state.get("completed_days", set())),
        "games_played": session_state.get("games_played", 0),
        "games_won":   session_state.get("games_won", 0),
        "submissions": session_state.get("submissions_count", 0),
    }


# ────────────────────────────────────────────────────────────
#  CERTIFICATE GENERATOR  (HTML → printable)
# ────────────────────────────────────────────────────────────
CERTIFICATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;600&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#f8f5ef; display:flex; align-items:center; justify-content:center; min-height:100vh; font-family:'DM Sans',sans-serif; }}
  .cert {{
    width:860px; padding:60px 80px;
    background:white;
    border:3px solid #cc0000;
    box-shadow: inset 0 0 0 12px #f8f5ef, inset 0 0 0 14px #f5c518;
    text-align:center; position:relative;
  }}
  .flag-bar {{ height:8px; background:linear-gradient(90deg,#000 33%,#cc0000 33% 66%,#f5c518 66%); margin-bottom:40px; }}
  .cert-header {{ font-size:.85rem; letter-spacing:.2em; text-transform:uppercase; color:#888; margin-bottom:16px; }}
  .cert-title {{ font-family:'Playfair Display',serif; font-size:3rem; color:#cc0000; margin-bottom:8px; }}
  .cert-sub {{ font-family:'Playfair Display',serif; font-style:italic; color:#888; font-size:1.1rem; margin-bottom:40px; }}
  .cert-body {{ font-size:.95rem; color:#555; line-height:1.8; margin-bottom:10px; }}
  .cert-name {{ font-family:'Playfair Display',serif; font-size:2.2rem; color:#0d0d0d; margin:14px 0; border-bottom:2px solid #f5c518; padding-bottom:10px; display:inline-block; min-width:300px; }}
  .cert-desc {{ font-size:.95rem; color:#555; margin-bottom:40px; line-height:1.8; }}
  .cert-meta {{ display:flex; justify-content:space-around; margin-top:50px; padding-top:20px; border-top:1px solid #eee; }}
  .cert-meta div {{ text-align:center; }}
  .cert-meta .label {{ font-size:.72rem; letter-spacing:.1em; text-transform:uppercase; color:#aaa; }}
  .cert-meta .value {{ font-size:1rem; font-weight:600; color:#0d0d0d; margin-top:4px; }}
  .badge {{ font-size:4rem; margin:20px 0; }}
  .flag-bar-bottom {{ height:8px; background:linear-gradient(90deg,#000 33%,#cc0000 33% 66%,#f5c518 66%); margin-top:40px; }}
</style>
</head>
<body>
<div class="cert">
  <div class="flag-bar"></div>
  <div class="cert-header">German Mastery Camp — Official Certificate</div>
  <div class="cert-title">Herzlichen Glückwunsch!</div>
  <div class="cert-sub">"Congratulations"</div>
  <div class="badge">🎓🇩🇪</div>
  <div class="cert-body">This is to certify that</div>
  <div class="cert-name">{name}</div>
  <div class="cert-desc">
    has successfully completed the <strong>90-Day German Mastery Camp</strong><br>
    demonstrating commitment, consistency, and a passion for the German language and culture.<br><br>
    <em>Total XP Earned: {xp} ⭐ &nbsp;|&nbsp; Longest Streak: {streak} days &nbsp;|&nbsp; Level: {level}</em>
  </div>
  <div class="cert-meta">
    <div>
      <div class="label">Completed On</div>
      <div class="value">{date}</div>
    </div>
    <div>
      <div class="label">CEFR Level Reached</div>
      <div class="value">{cefr}</div>
    </div>
    <div>
      <div class="label">Camp ID</div>
      <div class="value">#{cert_id}</div>
    </div>
  </div>
  <div class="flag-bar-bottom"></div>
</div>
</body>
</html>"""

def generate_certificate(name: str, xp: int, streak: int, level: str, cefr: str = "A2–B1") -> str:
    """Returns certificate as HTML string."""
    cert_id = hashlib.sha256(f"{name}{xp}{streak}".encode()).hexdigest()[:8].upper()
    return CERTIFICATE_HTML.format(
        name=name,
        xp=f"{xp:,}",
        streak=streak,
        level=level,
        date=datetime.date.today().strftime("%B %d, %Y"),
        cefr=cefr,
        cert_id=cert_id,
    )


# ────────────────────────────────────────────────────────────
#  ANALYTICS  (for Admin Panel charts)
# ────────────────────────────────────────────────────────────
def compute_platform_stats(users_df) -> dict:
    """Compute summary stats from Users DataFrame."""
    import pandas as pd
    if users_df.empty or "XP" not in users_df.columns:
        return {"total_users": 0, "active_today": 0, "avg_streak": 0, "total_xp": 0, "completion_rate": 0}

    total     = len(users_df)
    avg_streak = 0
    total_xp  = 0
    completions = 0

    for _, row in users_df.iterrows():
        try:
            days = json.loads(str(row.get("CompletedDays","[]")))
            if len(days) >= 90:
                completions += 1
        except Exception:
            pass
        try:
            total_xp += int(row.get("XP", 0))
        except Exception:
            pass
        try:
            avg_streak += int(row.get("Streak", 0))
        except Exception:
            pass

    return {
        "total_users":      total,
        "avg_streak":       round(avg_streak / max(total, 1), 1),
        "total_xp":         total_xp,
        "completion_rate":  round(completions / max(total, 1) * 100, 1),
    }

def xp_distribution(users_df) -> dict:
    """Returns XP bucket distribution for a histogram."""
    buckets = {"0–99": 0, "100–299": 0, "300–599": 0, "600–999": 0, "1000+": 0}
    if users_df.empty or "XP" not in users_df.columns:
        return buckets
    for xp in users_df["XP"].astype(int):
        if xp < 100:    buckets["0–99"] += 1
        elif xp < 300:  buckets["100–299"] += 1
        elif xp < 600:  buckets["300–599"] += 1
        elif xp < 1000: buckets["600–999"] += 1
        else:           buckets["1000+"] += 1
    return buckets

def days_completion_heatmap(users_df) -> list:
    """
    Returns list of 90 values: how many users have completed each day.
    """
    counts = [0] * 90
    if users_df.empty:
        return counts
    for _, row in users_df.iterrows():
        try:
            days = set(json.loads(str(row.get("CompletedDays","[]"))))
            for d in days:
                if 1 <= d <= 90:
                    counts[d - 1] += 1
        except Exception:
            pass
    return counts


# ────────────────────────────────────────────────────────────
#  EMAIL / WHATSAPP MESSAGE TEMPLATES
# ────────────────────────────────────────────────────────────
def generate_whatsapp_msg(top_name: str, day_num: int, done_names: list, missing_names: list) -> str:
    done_str    = ", ".join(done_names[:5]) + ("..." if len(done_names) > 5 else "")
    missing_str = ", ".join(missing_names[:5]) + ("..." if len(missing_names) > 5 else "")
    msg = f"""🇩🇪 *German Mastery Camp — Day {day_num} Update*

✅ خلصوا مهامهم النهارده ({len(done_names)} طالب):
{done_str}

⏳ لسه ما خلصوش ({len(missing_names)} طالب):
{missing_str}

🏆 أكتر واحد ملتزم النهارده: *{top_name}*

يلا يا جماعة! اليوم اللي بيفوت ميجيش تاني 💪
*Auf geht's! Ihr schafft das!* 🔥"""
    return msg

def generate_streak_reminder(name: str, streak: int, day: int) -> str:
    if streak > 0:
        return f"""مرحباً {name}! 👋

لا تكسر السلسلة! 🔥
عندك streak لـ *{streak} يوم* متتالي.
اليوم الـ *{day}* في انتظارك — خد 15 دقيقة دلوقتي.

«Ohne Fleiß kein Preis.» 🇩🇪
(بدون مجهود، بدون جايزة)"""
    else:
        return f"""مرحباً {name}! 👋

اليوم الـ *{day}* في انتظارك.
ابدأ streak جديد النهارده! 🔥

«Ein Schritt nach dem anderen führt zum Ziel.»
(خطوة خطوة توصل للهدف) 🇩🇪"""


# ────────────────────────────────────────────────────────────
#  GRAMMAR EXERCISE ENGINE
# ────────────────────────────────────────────────────────────
GRAMMAR_EXERCISES = {
    "article": [
        {"q":"___ Tisch ist groß.", "blanks":["Der","Die","Das"], "answer":"Der", "explain":"'Tisch' (table) is masculine → der"},
        {"q":"___ Lampe ist neu.", "blanks":["Der","Die","Das"], "answer":"Die", "explain":"'Lampe' (lamp) is feminine → die"},
        {"q":"___ Kind spielt.", "blanks":["Der","Die","Das"], "answer":"Das", "explain":"'Kind' (child) is neuter → das"},
        {"q":"Ich kaufe ___ Apfel.", "blanks":["den","die","das"], "answer":"den", "explain":"'Apfel' is masculine, accusative → den"},
        {"q":"Er gibt ___ Frau ein Buch.", "blanks":["der","die","den"], "answer":"der", "explain":"After 'geben', 'Frau' is dative → der"},
    ],
    "verb_conjugation": [
        {"q":"Ich ___ Student. (sein)", "blanks":["bin","bist","ist"], "answer":"bin", "explain":"ich → bin"},
        {"q":"Du ___ gut Deutsch. (sprechen)", "blanks":["sprichst","spreche","spricht"], "answer":"sprichst", "explain":"du + sprechen → sprichst (irregular: e→i)"},
        {"q":"Er ___ jeden Tag Kaffee. (trinken)", "blanks":["trinke","trinkst","trinkt"], "answer":"trinkt", "explain":"er/sie/es → -t ending"},
        {"q":"Wir ___ nach Berlin. (fahren)", "blanks":["fahren","fährt","fährst"], "answer":"fahren", "explain":"wir → fahren (infinitive form)"},
        {"q":"Ich ___ ein Buch lesen. (wollen)", "blanks":["will","willst","wollen"], "answer":"will", "explain":"Modal verb wollen: ich → will"},
    ],
    "word_order": [
        {"q":"Rearrange: [ich / lerne / jeden Tag / Deutsch]", "answer":"Ich lerne jeden Tag Deutsch.", "explain":"Standard SVO: Subject-Verb-Time-Object"},
        {"q":"Rearrange: [Deutsch / ich / lerne / weil / gut / möchte / sprechen / ich]", "answer":"Ich lerne Deutsch, weil ich gut sprechen möchte.", "explain":"'weil' is subordinating: verb goes to end of clause"},
        {"q":"Rearrange: [rufe / ich / meinen Bruder / an]", "answer":"Ich rufe meinen Bruder an.", "explain":"Separable verb: 'an' goes to end"},
    ],
}

def get_exercise_set(topic: str, count: int = 3) -> list:
    """Return a random set of exercises for a given grammar topic."""
    exercises = GRAMMAR_EXERCISES.get(topic, [])
    return random.sample(exercises, min(count, len(exercises))) if exercises else []


# ────────────────────────────────────────────────────────────
#  AI GRAMMAR FIXER (via Groq)
# ────────────────────────────────────────────────────────────
import requests
from config import GROQ_API_KEY


def ai_grammar_fixer(text: str) -> str:
    """Use Groq's Llama3-8b-8192 to correct German text."
    api_key = None
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY", GROQ_API_KEY)
    except Exception:
        api_key = GROQ_API_KEY
    if not api_key:
        return "⚠️ Groq API key not configured."

    prompt = (
        "You are a friendly German teacher. "
        "Correct the student's German and:\n"
        "1. Put the corrected sentence in **bold**.\n"
        "2. Explain each error in English.\n"
        "3. End with a short encouraging sentence in German.\n"
        f"\n\n{text}"
    )
    url = "https://api.groq.com/v1/requests"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "input": prompt, "max_output_tokens": 800}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        out = data.get("output", [])
        if out:
            return "".join(item.get("content","") for item in out)
        return "(no response)"
    except Exception as e:
        return f"AI error: {e}"
