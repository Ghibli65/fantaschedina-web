import streamlit as st
import os

# Configurazione Pagina
st.set_page_config(page_title="FantaSchedina - Login", layout="wide")

# CSS per Sidebar e Bottoni Gialli [cite: 2026-01-29]
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR [cite: 2026-01-29]
with st.sidebar:
    # Gestione sicura del Logo Ghiandaia
    if os.path.exists("ghiandaia imitatrice1.jpg"):
        st.image("ghiandaia imitatrice1.jpg", use_container_width=True)
    else:
        st.title("🏆 FantaSchedina")
    
    st.markdown("---")
    if st.button("🏠 Home / Login", use_container_width=True, type="primary"):
        st.rerun()
    if st.button("⚽ Vai al Gioco", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    
    # Logo Acquarossa in fondo
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if os.path.exists("WhatsApp Image 2026-01-30 at 12.59.32.jpeg"):
        st.image("WhatsApp Image 2026-01-30 at 12.59.32.jpeg", width=120)

# CORPO CENTRALE
col1, col_mid, col3 = st.columns([1, 1.2, 1])
with col_mid:
    st.markdown("<br><br><h1 style='text-align:center;'>BENVENUTO</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Area Accesso")
        st.text_input("Indirizzo Email")
        st.text_input("Password", type="password")
        if st.button("ENTRA NEL CAMPIONATO", use_container_width=True, type="primary"):
            st.info("Connessione in corso...")
