import streamlit as st

st.set_page_config(page_title="Caricamento", layout="wide")
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# Protezione: se non sei admin loggato, non vedi nulla
if not st.session_state.get("admin_logged_in"):
    st.error("Area riservata.")
    st.stop()

# --- MENU LATERALE EXCLUSIVE ADMIN ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica Quote", icon="🚀")

st.title("🚀 Caricamento Quote")
# ... (codice inserimento partite) ...
