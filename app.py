import streamlit as st
from supabase import create_client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS per nascondere il menu automatico e pulire lo stile
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione sessione
if "user" not in st.session_state: st.session_state.user = None

# --- MENU LATERALE RICHIESTO ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# --- CONTENUTO HOME ---
st.title("Benvenuto su FantaSchedina")
with st.form("login_form"):
    st.subheader("Login Utente")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.form_submit_button("ACCEDI"):
        st.info("Logica di accesso in corso...")
