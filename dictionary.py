import json
import streamlit as st
from pathlib import Path
from urllib.parse import quote

# load the preexisting vocabulary file
VOCAB_PATH = Path(__file__).parent / "vocabulary.json"

def load_vocab() -> dict:
    try:
        with open(VOCAB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def search_vocab(term: str) -> list:
    term = term.lower().strip()
    vocab = load_vocab()
    results = []
    for lvl, categories in vocab.items():
        for cat, words in categories.items():
            for w in words:
                if term in w.get("de","" ).lower() or term in w.get("en","").lower():
                    results.append({"level": lvl, "category": cat, **w})
    return results


def tts_url(word: str) -> str:
    # simple Google translate tts endpoint
    return f"https://translate.google.com/translate_tts?ie=UTF-8&tl=de&client=tw-ob&q={quote(word)}"


def add_personal_word(de: str, en: str):
    """Store personal word in a Google sheet or session state."""
    if st.session_state.get("user"):
        from data_manager import write_row
        write_row("WordBank", [st.session_state.user.get("Email"), de, en, ""])
    else:
        # fallback to session state list
        bank = st.session_state.setdefault("personal_bank", [])
        bank.append({"de":de,"en":en})
        st.session_state.personal_bank = bank


def load_personal_bank() -> list:
    if st.session_state.get("user"):
        from data_manager import load_sheet
        df = load_sheet("WordBank")
        if df.empty:
            return []
        return df.to_dict(orient="records")
    else:
        return st.session_state.get("personal_bank", [])
