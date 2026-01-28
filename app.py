import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# Nasconde i link grigi automatici in alto a sinistra
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- MENU LATERALE ---
st.sidebar.title("🏆 Menu Principale")

# Link Home
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")

# Link diretti ai file (Usiamo i percorsi che hai su GitHub)
try:
    st.sidebar.page_link("pagine_app/2_Registrazione.py", label="Registrazione Utente", icon="📝")
    st.sidebar.page_link("pagine_app/3_Admin.py", label="Accesso Admin", icon="🔐")
    
    if st.session_state.user:
        st.sidebar.divider()
        st.sidebar.page_link("pagine_app/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")
except Exception as e:
    st.sidebar.error("Verifica i nomi dei file su GitHub")

# --- CONTENUTO HOME ---
if st.session_state.user is None:
    st.title("Benvenuto su FantaSchedina")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("Credenziali non valide.")
else:
    st.title(f"Bentornato! 👋")
    st.info(f"Sei loggato come: {st.session_state.user.email}")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
