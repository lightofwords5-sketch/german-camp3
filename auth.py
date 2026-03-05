import bcrypt
import datetime
from typing import Optional

from data_manager import load_sheet, write_row

# Authentication helpers moved out of app.py for modularity

def hash_pw(password: str) -> str:
    """Return bcrypt hash of password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_pw(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def get_user(email: str) -> Optional[dict]:
    df = load_sheet("Users")
    if df.empty or "Email" not in df.columns:
        return None
    row = df[df["Email"].str.lower() == email.lower()]
    return row.iloc[0].to_dict() if not row.empty else None


def register_user(name: str, email: str, password: str) -> bool:
    if get_user(email):
        return False
    hashed = hash_pw(password)
    now = datetime.datetime.now().isoformat()
    return write_row("Users", [name, email, hashed, 0, 0, 1, 0, now, ""])


def login_user(email: str, password: str):
    user = get_user(email)
    if user and check_pw(password, str(user.get("Password", ""))):
        return user
    return None


def update_user_xp(email: str, new_xp: int, new_streak: int, completed_days_json: str):
    """Bulk update XP, streak, and completed days for a user."""
    from data_manager import get_gsheet_client

    client = get_gsheet_client()
    if not client:
        return
    try:
        sheet_id = None
        try:
            import streamlit as st
            sheet_id = st.secrets.get("sheet_id")
        except Exception:
            pass
        if not sheet_id:
            return
        wk = client.open_by_key(sheet_id).worksheet("Users")
        records = wk.get_all_records()
        headers = wk.row_values(1)
        for i, row in enumerate(records, start=2):
            if str(row.get("Email", "")).lower() == email.lower():
                xp_col = headers.index("XP") + 1
                streak_col = headers.index("Streak") + 1
                days_col = headers.index("CompletedDays") + 1
                wk.update_cell(i, xp_col, new_xp)
                wk.update_cell(i, streak_col, new_streak)
                wk.update_cell(i, days_col, completed_days_json)
                break
        # clear cache in loader
        from data_manager import load_sheet
        load_sheet.clear()
    except Exception as e:
        try:
            import streamlit as st
            st.error(f"XP update error: {e}")
        except Exception:
            pass
