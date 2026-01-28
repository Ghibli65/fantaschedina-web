import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS per nascondere il menu automatico e abbellire i link
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- MENU LATERALE ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

if st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pages/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state.user = None
        st.rerun()

# --- LOGICA LOGIN ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto su FantaSchedina")
    st.subheader("Accedi per iniziare")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI", use_container_width=True):
            try:
                res = st.session_state.supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("Accesso effettuato!")
                st.rerun()
            except:
                st.error("Credenziali non valide.")
else:
    st.title(f"Ciao!")
    st.success(f"Sei loggato come: **{st.session_state.user.email}**")
    st.info("👈 Seleziona una voce dal menu laterale per continuare.")
