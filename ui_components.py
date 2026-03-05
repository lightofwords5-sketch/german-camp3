import streamlit as st
from config import tr


# CSS injection for theme, glassmorphism and dark/light toggle

CSS_LOADED = False

def inject_css():
    global CSS_LOADED
    if CSS_LOADED:
        return
    CSS_LOADED = True
    css = open("styles.css").read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_xp_bar():
    done = len(st.session_state.completed_days)
    xp = st.session_state.get("user_xp", 0)
    streak = st.session_state.get("streak", 0)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📅 " + tr("days"), f"{min(done+1,90)}/90")
    c2.metric("⭐ " + tr("xp"),  xp)
    c3.metric("🔥 " + tr("streak"), f"{streak}d")
    c4.metric("✅ " + tr("completed"), done)


def language_selector():
    with st.sidebar:
        lang = st.radio("", options=["English", "العربية"], index=0 if st.session_state.get("lang","en") == "en" else 1)
        st.session_state["lang"] = "en" if lang == "English" else "ar"


def render_sidebar():
    inject_css()
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:10px 0 16px;'>
            <div style='font-size:2.2rem;'>🇩🇪</div>
            <div style='font-family:"Playfair Display",serif;font-size:1.2rem;color:#f5c518;font-weight:700;'>German Mastery Camp</div>
            <div style='color:#555;font-size:.78rem;margin-top:2px;'>90-Day Intensive</div>
        </div>""", unsafe_allow_html=True)
        # language switcher
        language_selector()

        if st.session_state.logged_in and st.session_state.user:
            name = st.session_state.user.get("Name","Learner")
            admin_tag = ''
            if st.session_state.get("is_admin"):
                admin_tag = ' <span class="admin-badge">ADMIN</span>'
            st.markdown(f"""
            <div style='text-align:center;margin-bottom:12px;'>
                <div style='font-size:1.8rem;'>{"⚙️" if st.session_state.get("is_admin") else "👤"}</div>
                <div style='font-weight:600;font-size:.95rem;'>{name}{admin_tag}</div>
                <div style='color:#555;font-size:.75rem;'>⭐ {st.session_state.get("user_xp",0)} XP</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        pages = {
            tr("home_title"): "home",
            tr("roadmap_title"): "roadmap",
            tr("daily_mission"): "daily",
            tr("chat_placeholder"): "ai",
            tr("dictionary_title"): "dictionary",
            tr("output_title"): "output",
            "🎮 Mini Games": "games",
            "🏆 Leaderboard": "leaderboard",
            "🔬 Phonetics Lab": "phonetics",
            "📚 Resources": "resources",
        }
        if st.session_state.get("is_admin"):
            pages[tr("admin_panel")] = "admin"

        for label, key in pages.items():
            active = st.session_state.current_page == key
            style = "color:#f5c518!important;" if active else ""
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")
        # mini progress
        done = len(st.session_state.completed_days)
        st.markdown(f"**{tr('progress')}: {done}/90 days**")
        st.progress(done / 90)
        streak = st.session_state.get("streak",0)
        xp = st.session_state.get("user_xp",0)
        st.markdown(f"<div style='display:flex;justify-content:space-between;color:#888;font-size:.82rem;'><span>🔥 {streak} {tr('days')}</span><span>⭐ {xp} {tr('xp')}</span></div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button(f"🚪 {tr('logout')}", key="signout"):
            # call external save_progress if exists
            if hasattr(st.session_state, 'save_progress'):
                st.session_state.save_progress()
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
