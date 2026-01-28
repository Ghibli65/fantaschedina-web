import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione")

# --- STESSO CSS DI APP.PY ---
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# --- STESSA SIDEBAR DI APP.PY ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

st.title("📝 Registrazione")
# ... (tuo codice registrazione qui) ...
