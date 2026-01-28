import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# --- IL TRUCCO MAGICO PER IL MENU ---
st.markdown("""
    <style>
    /* Nasconde i link automatici 'grigi' di Streamlit */
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Rende i tuoi bottoni del menu più belli */
    .stPageLink {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "user" not in st.session_state: st.session_state.user = None

# --- MENU LATERALE PERSONALIZZATO ---
st.sidebar.title("🏆 Menu Principale")

# Link sicuri verso la cartella 'pages'
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

if st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pages/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

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
    st.title(f"Ciao! 👋")
    st.success(f"Loggato come: {st.session_state.user.email}")
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state.user = None
        st.rerun()
