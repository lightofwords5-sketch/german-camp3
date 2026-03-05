# 🇩🇪 German Mastery Camp

> A gamified 90-day German language learning platform built with Streamlit.  
> Open registration · AI Copilot · Admin Panel · Locked Progression · Mini Games

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red) ![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Auth** | Open email registration + separate admin password login |
| 🗺️ **Roadmap** | Visual 90-day path with Duolingo-style locked progression |
| 📅 **Daily Mission** | 120-min checklist with embedded YouTube videos |
| 🤖 **AI Copilot "Klaus"** | Grammar fixer + 24/7 chat (powered by Groq Llama3) |
| 🎮 **Mini Games** | Flashcard Quiz · Word Match · Sentence Scramble |
| 🏆 **Leaderboard** | XP + Streak rankings synced to Google Sheets |
| 🔬 **Phonetics Lab** | 6 sound cards + minimal pairs practice |
| ⚙️ **Admin Panel** | Add content · Monitor students · View submissions |
| 📊 **Google Sheets DB** | `Users` · `Content` · `Submissions` tabs |

---

## 🚀 Quick Deploy (Free)

```bash
# 1. Push app.py + requirements.txt to a public GitHub repo
# 2. Go to share.streamlit.io → New App → select repo → app.py
# 3. Paste secrets in Advanced Settings → Deploy ✅
```

Live at: `https://your-name-german-camp.streamlit.app`

---

## 📁 Project Structure

```
german-mastery-camp/
├── app.py              # Main application (~600 lines)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── SETUP_GUIDE.md      # Full Google Sheets + secrets guide
└── .streamlit/
    └── secrets.toml    # API keys & credentials (local only, never commit)
```

---

## ⚙️ secrets.toml Template

```toml
sheet_id          = "YOUR_GOOGLE_SHEET_ID"
admin_password    = "your_secret_password"
GROQ_API_KEY = "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"  # or your own

[gcp_service_account]
type          = "service_account"
project_id    = "your-project"
private_key   = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email  = "your-service@project.iam.gserviceaccount.com"
# ... full service account JSON fields
```

> See **SETUP_GUIDE.md** for the complete Google Sheet schema and step-by-step instructions.

---

## 🗂️ Google Sheet Schema (3 tabs)

| Tab | Key Columns |
|---|---|
| `Users` | Name · Email · Password · XP · Streak · CompletedDays · JoinedAt |
| `Content` | Day_Number · Phase · Topic · Video_ID · Anki_Task · Writing_Task · Reading_Text |
| `Submissions` | Name · Email · OriginalText · CorrectedText · SubmittedAt |

---

## 🏃 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Demo Mode:** Without secrets.toml, the app runs fully in-memory — no setup needed for testing.

---

## 🔑 Admin Access

Enter your `admin_password` in the **"Admin password"** field on the login screen → **Admin Login**.  
The admin panel lets you add daily missions, monitor student completion, and review AI-corrected writing — all from the UI, zero code changes needed.

---

## ⭐ XP System

| Action | XP |
|---|---|
| Complete all 4 daily tasks | +20 |
| Flashcard Quiz round | +10 |
| Word Match game | +15 |
| Sentence Scramble | +20 |

---

*Viel Erfolg! 🇩🇪*
