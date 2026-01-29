import streamlit as st

st.set_page_config(page_title="Admin", layout="wide")
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# Verifica accesso Admin
if not st.session_state.get("admin_logged_in"):
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")
    
    st.title("🔐 Accesso Amministratore")
    u = st.text_input("Utente Admin")
    p = st.text_input("Password Admin", type="password")
    if st.button("Sblocca"):
        if u == "Admin" and p == "fanta":
            st.session_state.admin_logged_in = True
            st.rerun()
        else: st.error("Accesso negato")
    st.stop()

# --- MENU LATERALE EXCLUSIVE ADMIN ---
st.sidebar.title("⚙️ Pannello Admin")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica Quote", icon="🚀") # Appare SOLO QUI

if st.sidebar.button("Chiudi Sessione Admin"):
    del st.session_state.admin_logged_in
    st.rerun()

st.title("Pannello di Controllo Admin")
st.info("Da qui gestisci l'intera applicazione. Il menu a sinistra è ora dedicato alle funzioni admin.")
