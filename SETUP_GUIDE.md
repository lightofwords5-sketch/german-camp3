# 🇩🇪 German Mastery Camp — Professional Edition
## Complete Setup & Deployment Guide

---

## 🗂️ Step 1 — Google Sheet Setup

Create a **Google Sheet** with these 4 tabs (exact names):

### Tab 1: `Users`
| Name | Email | Password | XP | Streak | DaysCompleted | CompletedDays | JoinedAt | GoogleID |
|------|-------|----------|----|--------|---------------|---------------|----------|----------|
| (leave empty — app fills this) |

### Tab 2: `Content`
| Day_Number | Phase | Topic | Video_Link_Arabic | Video_ID | Anki_Task | Pronunciation_Task | Writing_Task | Reading_Text |
|---|---|---|---|---|---|---|---|---|
| 1 | Foundation | Alphabet & Phonetics | https://youtube.com/... | dQw4w9WgXcQ | Add 15 alphabet cards | Practice ä ö ü on YouGlish | Write alphabet 3 times | Der Buchstabe A... |
| 2 | Foundation | Numbers 1–20 | https://youtube.com/... | YOUTUBE_ID | Add 20 number cards | Say numbers aloud | Write 1–20 in German | |

> **⚠️ Video_ID**: Only paste the part AFTER `v=` in a YouTube URL.
> Example: `https://youtube.com/watch?v=XbiBS5YIQB0` → paste `XbiBS5YIQB0`

### Tab 3: `Submissions`
| Name | Email | OriginalText | CorrectedText | SubmittedAt |
|------|-------|--------------|---------------|-------------|
| (leave empty — app fills this) |

---

## 🔑 Step 2 — Google Service Account

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → Enable **Google Sheets API** + **Google Drive API**
3. Go to **Credentials** → Create **Service Account**
4. Download the JSON key file
5. **Share your Google Sheet** with the service account email (Editor access)

---

## 🔐 Step 3 — Streamlit Secrets

Create `.streamlit/secrets.toml` locally (or paste in Streamlit Cloud → App Settings → Secrets):

```toml
# Your Google Sheet ID (from the URL)
sheet_id = "YOUR_GOOGLE_SHEET_ID_HERE"

# Admin password for the admin panel
admin_password = "your_secret_admin_password"

# Groq API key for AI Copilot
GROQ_API_KEY = "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"

# Paste your entire service account JSON here
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

---

## 🚀 Step 4 — Deploy on Streamlit Cloud (Free)

```
your-repo/
├── app.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml   ← (local only, add in cloud dashboard)
```

1. Push `app.py` + `requirements.txt` to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select your repo → `app.py`
4. Go to **Advanced settings** → paste your secrets
5. Deploy → live at `your-name-german-camp.streamlit.app` ✅

---

## 🖥️ Local Testing

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Demo Mode:** If no secrets.toml is configured, the app runs in demo mode —  
> anyone can log in with any email/password and progress is stored in session only.

---

## 🔑 Admin Panel Access

On the login screen:
- Leave email/password blank
- Enter your `admin_password` from secrets.toml in the **Admin password** field
- Click **Admin Login**

Admin features:
- Add/edit daily missions directly from the UI (no code needed)
- See which students completed today vs. not
- View all writing submissions with AI corrections
- Generate WhatsApp status messages for your group

---

## 📱 Features Summary

| Feature | Description |
|---|---|
| 🔐 Auth | Email registration (anyone can join) + admin password login |
| 🗺️ Roadmap | Visual path with locked/unlocked days |
| 📅 Daily Mission | 120-min checklist with YouTube embed + reading text |
| 🤖 AI Copilot | Grammar fixer + 24/7 chat with "Klaus" (Groq Llama3) |
| 🎮 Games | Flashcard Quiz, Word Match, Sentence Scramble |
| 🏆 Leaderboard | XP + Streak rankings, live from Google Sheet |
| 🔬 Phonetics Lab | 6 sound cards + minimal pairs practice |
| ⚙️ Admin Panel | Add content, monitor students, view submissions |
| 📊 Google Sheets DB | Users, Content, Submissions tabs |

---

## ⭐ XP System

| Action | XP Earned |
|---|---|
| Complete all 4 daily tasks | +20 XP |
| Win a Flashcard Quiz round | +10 XP |
| Win a Word Match game | +15 XP |
| Solve Sentence Scramble | +20 XP |
| Submit writing to AI fixer | logged for admin |

---

*Viel Erfolg! 🇩🇪*
