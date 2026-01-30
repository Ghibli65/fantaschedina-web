import streamlit as st
from supabase import create_client, Client
import os

# Configurazione Wide e Titolo
st.set_page_config(page_title="FantaSchedina - Home", layout="wide")

# CSS per Sfondo Azzurro Polvere e Sidebar Fissa
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; } /* Sfondo azzurro polvere chiarissimo */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Box Login Bianco e Pulito */
    .stForm {
        background-color: white !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    
    /* Titolo Home */
    .welcome-header {
        color: #1e3c72;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR PROFESSIONALE ---
with st.sidebar:
    # Gestione Errore Logo 1
    if os.path.exists("logo1.png"):
        st.image("logo1.png", width=160)
    else:
        st.title("🏆 FantaSchedina")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigazione Utente
    if st.button("🏠 Home / Login", use_container_width=True, type="primary"):
        st.switch_page("app.py")
    if st.button("⚽ Gioca Ora", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    
    # Spazio vuoto per spingere il secondo logo in basso
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # Logo 2 (FantaSchedina circolare) in fondo alla sidebar
    if os.path.exists("logo2.png"):
        st.divider()
        st.image("logo2.png", width=130)
        st.caption("Official Partner App")

# --- CORPO CENTRALE ---
col_1, col_center, col_3 = st.columns([1, 1.5, 1])

with col_center:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='welcome-header'>BENVENUTO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5a7184; margin-bottom:30px;'>Accedi al pannello per gestire le tue giocate</p>", unsafe_allow_html=True)
    
    with st.form("Login Form"):
        st.markdown("### Area Accesso")
        email = st.text_input("Indirizzo Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("ENTRA NEL CAMPIONATO", use_container_width=True)
        
        if submit:
            # Qui andrà la tua logica Supabase
            st.info("Verifica credenziali in corso...")

    # Footer estetico sotto il login
    st.markdown("<br><p style='text-align:center; font-size:12px; color:#94a3b8;'>FantaSchedina v2.0 Professional Edition • 2026</p>", unsafe_allow_html=True)
