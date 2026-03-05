import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource(ttl=60)
def get_gsheet_client():
    """Returns authenticated gspread client using service account from secrets."""
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception:
        return None

@st.cache_data(ttl=30)
def load_sheet(sheet_name: str) -> pd.DataFrame:
    """Load a worksheet tab as a DataFrame (cached 30 s)."""
    client = get_gsheet_client()
    if client is None:
        return pd.DataFrame()
    try:
        sheet_id = st.secrets.get("sheet_id")
        wk = client.open_by_key(sheet_id).worksheet(sheet_name)
        return pd.DataFrame(wk.get_all_records())
    except Exception:
        return pd.DataFrame()


def write_row(sheet_name: str, row: list):
    """Append a row to a worksheet."""
    client = get_gsheet_client()
    if client is None:
        return False
    try:
        sheet_id = st.secrets.get("sheet_id")
        wk = client.open_by_key(sheet_id).worksheet(sheet_name)
        wk.append_row(row, value_input_option="USER_ENTERED")
        load_sheet.clear()
        return True
    except Exception as e:
        st.error(f"Sheet write error: {e}")
        return False


def update_cell_by_key(sheet_name: str, key_col: str, key_val, target_col: str, new_val):
    """Update a single cell identified by key column."""
    client = get_gsheet_client()
    if client is None:
        return
    try:
        sheet_id = st.secrets.get("sheet_id")
        wk = client.open_by_key(sheet_id).worksheet(sheet_name)
        records = wk.get_all_records()
        headers = wk.row_values(1)
        key_idx = headers.index(key_col) + 1
        tgt_idx = headers.index(target_col) + 1
        for i, row in enumerate(records, start=2):
            if str(row.get(key_col)) == str(key_val):
                wk.update_cell(i, tgt_idx, new_val)
                break
        load_sheet.clear()
    except Exception as e:
        st.error(f"Update error: {e}")
