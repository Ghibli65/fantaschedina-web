import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS DEFINITIVO: Nasconde la lista file automatica e pulisce il menu
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton>button {width: 100%; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- BARRA LATERALE PERSONALIZZATA ---
st.sidebar.title("🏆 Menu Principale")

# Usiamo switch_page per la Home per evitare errori di link
if st.sidebar.button("👤 Home / Login"):
    st.switch_page("app.py")

st.sidebar.divider()

# Link ai file nella cartella 'pagine_app' (percorsi verificati dal tuo GitHub)
try:
    st.sidebar.page_link("pagine_app/2_Registrazione.py", label="Registrazione Utente", icon="📝")
    st.sidebar.page_link("pagine_app/3_Admin.py", label="Accesso Admin", icon="🔐")
    
    if st.session_state.user:
        st.sidebar.page_link("pagine_app/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")
except Exception:
    st.sidebar.error("Verifica nomi file in 'pagine_app'")

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
    st.success(f"Loggato come: {st.session_state.user.email}")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.user = None
        st.rerun()
