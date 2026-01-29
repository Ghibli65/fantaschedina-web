import streamlit as st
from supabase import create_client

# Configurazione della pagina
st.set_page_config(page_title="FantaSchedina", layout="wide")

# --- INIZIALIZZAZIONE SUPABASE CON CONTROLLO ERRORI ---
if "supabase" not in st.session_state:
    try:
        # Recupero credenziali dai Secrets [cite: 2026-01-29]
        url = st.secrets.get("supabase_url")
        key = st.secrets.get("supabase_key")
        
        if not url or not key:
            st.error("🚨 Errore: Credenziali Supabase mancanti nei Secrets!")
            st.stop()
            
        st.session_state.supabase = create_client(url, key)
    except Exception as e:
        st.error(f"🚨 Errore di connessione a Supabase: {e}")
        st.stop()

# --- CSS PERSONALIZZATO (Senza barre e pulito) ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .login-container {max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE DI LOGOUT ---
def logout_process():
    if "user" in st.session_state:
        del st.session_state["user"]
    st.rerun()

# --- SIDEBAR ---
st.sidebar.title("🏆 FantaSchedina")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")

if "user" in st.session_state:
    st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")
    st.sidebar.divider()
    if st.sidebar.button("🚪 ESCI", use_container_width=True):
        logout_process()
else:
    st.sidebar.page_link("pages/2_Registrazione.py", label="📝 Registrazione", icon="📩")
    st.sidebar.page_link("pages/3_Admin.py", label="🔐 Accesso Admin", icon="🕵️")

# --- CONTENUTO HOME ---
if "user" in st.session_state:
    st.title(f"Bentornato!")
    st.success(f"Loggato come: {st.session_state.user.email}")
    st.write("Seleziona **GIOCA ORA** dal menu a sinistra per inserire i tuoi pronostici.")
else:
    st.title("⚽ Benvenuto su FantaSchedina")
    st.write("Accedi per partecipare al campionato.")
    
    with st.container():
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("ACCEDI", type="primary", use_container_width=True):
            try:
                # Tentativo di login [cite: 2026-01-29]
                auth = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = auth.user
                st.rerun()
            except:
                st.error("Credenziali non valide.")
