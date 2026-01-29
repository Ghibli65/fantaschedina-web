import streamlit as st
from supabase import create_client

# Configurazione della pagina
st.set_page_config(page_title="FantaSchedina", layout="wide")

# Inizializzazione Supabase
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["supabase_url"], 
        st.secrets["supabase_key"]
    )

# --- CSS DESIGN ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .user-info-box {padding: 15px; background-color: #f0f4f8; border-radius: 12px; border-left: 5px solid #1e3c72; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE DI LOGOUT ---
def logout_process():
    # Rimuoviamo solo le chiavi legate all'utente per sicurezza
    if "user" in st.session_state:
        del st.session_state["user"]
    st.rerun()

# --- SIDEBAR DINAMICA ---
st.sidebar.title("🏆 FantaSchedina")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")

if "user" in st.session_state:
    st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")
    st.sidebar.divider()
    if st.sidebar.button("🚪 ESCI (Logout)", use_container_width=True):
        logout_process()
else:
    st.sidebar.page_link("pages/2_Registrazione.py", label="📝 Registrazione", icon="📩")
    st.sidebar.page_link("pages/3_Admin.py", label="🔐 Accesso Admin", icon="🕵️")

# --- CONTENUTO DELLA PAGINA ---
if "user" in st.session_state:
    st.title("Benvenuto nel Team!")
    st.markdown(f"""
        <div class="user-info-box">
            👤 <b>Utente:</b> {st.session_state.user.email}<br>
            📅 <b>Stato:</b> Account Attivo
        </div>
    """, unsafe_allow_html=True)
    st.write("Scegli **'GIOCA ORA'** dal menu a sinistra per inserire i tuoi pronostici.")
else:
    st.title("⚽ FantaSchedina")
    st.write("Accedi per iniziare a sfidare i tuoi amici.")
    
    # Login Form
    with st.container():
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("ACCEDI AL SISTEMA", type="primary", use_container_width=True):
            if email and pwd:
                try:
                    # Tentativo di autenticazione [cite: 2026-01-28]
                    auth_response = st.session_state.supabase.auth.sign_in_with_password({
                        "email": email, 
                        "password": pwd
                    })
                    # Salviamo l'utente e forziamo il ricaricamento immediato [cite: 2026-01-28]
                    st.session_state.user = auth_response.user
                    st.rerun() 
                except Exception as e:
                    st.error("Credenziali errate. Controlla email e password.")
            else:
                st.warning("Inserisci sia email che password.")
