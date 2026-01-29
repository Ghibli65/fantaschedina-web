import streamlit as st
from supabase import create_client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# --- CSS PER BLOCCO MENU AUTOMATICO E STILE PULITO ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase e Sessione
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "user" not in st.session_state: 
    st.session_state.user = None

# --- MENU LATERALE FISSO ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# --- CONTENUTO HOME ---
st.title("Benvenuto su FantaSchedina")

if st.session_state.user is None:
    with st.form("login_form"):
        st.subheader("Login Utente")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Accesso effettuato!")
                st.rerun()
            except:
                st.error("Credenziali non valide.")
else:
    st.success(f"Loggato come: {st.session_state.user.email}")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.user = None
        st.rerun()
