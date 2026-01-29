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

# --- CSS PER L'INTERFACCIA ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .user-info-box {padding: 15px; background-color: #f0f4f8; border-radius: 12px; border-left: 5px solid #1e3c72; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE DI LOGOUT ---
def logout_process():
    for key in list(st.session_state.keys()):
        if key != "supabase": # Teniamo solo la connessione al DB
            del st.session_state[key]
    st.rerun()

# --- SIDEBAR DINAMICA ---
st.sidebar.title("🏆 FantaSchedina")
st.sidebar.page_link("app.py", label="Home / Login", icon="🏠")

if "user" in st.session_state:
    # Menu visibile solo se loggato
    st.sidebar.page_link("pages/1_Gioca.py", label="⚽ GIOCA ORA", icon="⚽")
    st.sidebar.divider()
    if st.sidebar.button("🚪 ESCI (Logout)", use_container_width=True):
        logout_process()
else:
    # Menu visibile se non loggato
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
    st.write("Scegli **'GIOCA ORA'** dal menu a sinistra per inserire i tuoi pronostici della settimana.")
else:
    st.title("⚽ FantaSchedina")
    st.write("Accedi con le tue credenziali per iniziare a giocare.")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI", use_container_width=True):
            try:
                auth = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = auth.user
                st.success("Accesso riuscito! Reindirizzamento...")
                st.rerun()
            except:
                st.error("Credenziali non valide. Riprova.")
