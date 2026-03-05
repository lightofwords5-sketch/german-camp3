# Contributing to German Mastery Camp 🇩🇪

Thank you for wanting to contribute! This is an open-source project — anyone can improve it.

---

## 🚀 Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/german-mastery-camp.git
cd german-mastery-camp
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py               # Main application & routing
├── config.py            # All constants, phases, badges, XP rules
├── utils.py             # SRS algorithm, badges, certificate, analytics
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .streamlit/
│   └── config.toml      # Theme
└── data/
    ├── curriculum.json  # 90-day content structure
    └── vocabulary.json  # 520+ German words by level/category
```

---

## 🤝 Ways to Contribute

### 1. Add Curriculum Content
Edit `data/curriculum.json` to fill in missing days or improve existing ones:
- Add real YouTube video IDs
- Improve reading texts
- Add better example sentences
- Add Arabic bridge video IDs for Days 1–14

### 2. Expand the Vocabulary Bank
Edit `data/vocabulary.json`:
- Add more word categories
- Add B2/C1 level words
- Add audio_url fields when sources are found

### 3. Add Grammar Exercises
Edit the `GRAMMAR_EXERCISES` dict in `utils.py`:
- Add more exercise types (matching, fill-blank, translation)
- Cover more grammar topics

### 4. Improve Games
In `app.py`, find `page_games()` and add:
- Listening exercises with audio
- Picture→word matching
- Conjugation drills

### 5. Translations / Localization
Help translate the UI for Arabic speakers who prefer Arabic instructions.

---

## 📋 Contribution Rules

- Keep commits focused — one feature or fix per PR
- Test locally before submitting a PR
- Don't commit `.streamlit/secrets.toml`
- Document new config options in README

---

## 🐛 Reporting Bugs

Open a GitHub Issue with:
1. What you expected
2. What happened instead
3. Steps to reproduce

---

*Viel Erfolg! 🇩🇪*
