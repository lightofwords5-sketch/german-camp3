import requests
import streamlit as st
from config import GROQ_API_KEY

# AI helpers using Groq Llama3 model

def _groq_request(prompt: str, max_tokens: int = 800) -> str:
    api_key = st.secrets.get("GROQ_API_KEY", GROQ_API_KEY)
    if not api_key:
        return "⚠️ AI API key not configured. Please set GROQ_API_KEY in secrets."
    url = "https://api.groq.com/v1/requests"
    payload = {
        "model": "llama3-8b-8192",
        "input": prompt,
        "max_output_tokens": max_tokens,
        # other parameters could be added here
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # Groq returns an "output" field with list of content pieces
        out = data.get("output", [])
        if out:
            # concatenate all text chunks
            return "".join(chunk.get("content","") for chunk in out)
        return ""
    except Exception as e:
        return f"AI error: {e}"


def ai_grammar_fixer(text: str) -> str:
    """Take German text and return a corrected version with explanations."""
    system = (
        "You are an expert German tutor. Correct the student's text and:\n"
        "1. Provide the corrected version in bold.\n"
        "2. List each error with a clear explanation in English.\n"
        "3. End with one encouraging sentence in German.\n"
        "Keep responses concise and educational."
    )
    prompt = f"{system}\n\n{text}"
    return _groq_request(prompt, max_tokens=1000)


def ai_chat(messages: list, user_msg: str) -> str:
    """Simple conversational helper using Groq.
    `messages` is a list of dicts with 'role' and 'content'.
    """
    # keep last 10 messages
    history = messages[-10:]
    conversation = "".join([f"{m['role']}: {m['content']}\n" for m in history])
    prompt = (
        "You are Klaus, a friendly German language tutor AI.\n"
        "Help students with grammar, vocabulary, culture, and pronunciation.\n"
        "When giving German examples, always include the English translation.\n"
        "Keep answers concise.\n"
        f"{conversation}user: {user_msg}\nassistant:"
    )
    return _groq_request(prompt, max_tokens=600)
