import streamlit as st
from supabase import create_client, Client
import os

st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS: Nasconde i link grigi automatici e pulisce il menu
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "user" not in st.session_state: st.session_state.user = None

# --- MENU LATERALE ---
st.sidebar.title("🏆 Menu Principale")

if st.sidebar.button("🏠 Home / Login", use_container_width=True):
    st.switch_page("app.py")

st.sidebar.divider()

# Funzione per creare link sicuri
def crea_link(percorso, etichetta, icona):
    # Controlla se il file esiste davvero [cite: 2026-01-28]
    if os.path.exists(percorso):
        st.sidebar.page_link(percorso, label=etichetta, icon=icona)
    else:
        # Se fallisce, ci dice cosa vede il server [cite: 2026-01-28]
        st.sidebar.error(f"❌ Non trovo: {percorso}")

# Prova a creare i link con i percorsi relativi
crea_link("pagine_app/2_Registrazione.py", "Registrazione Utente", "📝")
crea_link("pagine_app/3_Admin.py", "Accesso Admin", "🔐")

if st.session_state.user:
    st.sidebar.divider()
    crea_link("pagine_app/1_Gioca.py", "VAI A GIOCARE", "⚽")

# --- CONTENUTO HOME ---
if st.session_state.user is None:
    st.title("Benvenuto su FantaSchedina")
    with st.form("login"):
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Credenziali errate")
else:
    st.title(f"Bentornato! 👋")
    st.success(f"Loggato come: {st.session_state.user.email}")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.user = None
        st.rerun()
