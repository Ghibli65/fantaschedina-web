import streamlit as st
import os

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaSchedina - Login", layout="wide")

# 2. CSS Avanzato per distanziare i loghi e pulire il fondo
st.markdown("""
    <style>
    /* Fondo azzurro polvere/grigio professionale */
    .stApp { background-color: #f8fafc; }
    
    /* Nasconde il menu di navigazione automatico */
    [data-testid="stSidebarNav"] {display: none;}

    /* Centratura del modulo di login */
    .auth-container {
        max-width: 400px;
        margin: auto;
        padding-top: 50px;
    }

    /* Stile Sidebar per bloccare i loghi */
    section[data-testid="stSidebar"] > div {
        display: flex;
        flex-direction: column;
        justify-content:空间-between;
        height: 100vh;
    }

    /* Bottone Login Giallo */
    .stButton > button[kind="primary"] {
        background-color: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CON LOGHI DISTANZIATI ---
with st.sidebar:
    # PARTE ALTA: Logo Ghiandaia e Titolo
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("logo1.png"):
        st.image("logo1.png", use_container_width=True)
    else:
        st.title("🏆 FantaSchedina")
    
    st.markdown("---")
    
    # Navigazione
    if st.button("🏠 Home / Login", type="primary", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Gioca Ora", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")
    
    # Spazio flessibile per spingere il secondo logo in fondo
    st.write("") # placeholder
    
    # PARTE BASSA: Logo Acquarossa (Circolare)
    # Usiamo un container per posizionarlo fisso in basso
    with st.container():
        st.markdown("<br><br><br><br>", unsafe_allow_html=True) # Spinta extra
        if os.path.exists("logo2.png"):
            st.image("logo2.png", width=150)
        st.caption("Developed by Acquarossa • 2026")

# --- CORPO CENTRALE (LOGIN) ---
col1, col_center, col3 = st.columns([1, 1.2, 1])

with col_center:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    # Logo centrale se vuoi rinforzare il brand (opzionale)
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>BENVENUTO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Inserisci le tue credenziali per entrare</p>", unsafe_allow_html=True)
    
    # Box di Login pulito
    with st.container(border=True):
        st.markdown("### Area Accesso")
        email = st.text_input("Indirizzo Email")
        password = st.text_input("Password", type="password")
        
        if st.button("ENTRA NEL CAMPIONATO", type="primary", use_container_width=True):
            # Qui andrà il collegamento a Supabase
            st.info("Verifica in corso...")

    st.markdown("<p style='text-align: center; font-size: 11px; color: #94a3b8; margin-top: 20px;'>FantaSchedina Professional v2.0</p>", unsafe_allow_html=True)
