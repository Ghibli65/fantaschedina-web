import streamlit as st
from supabase import create_client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# --- CSS PER BLOCCARE IL MENU (COPIALO IN TUTTE LE PAGINE) ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

if "user" not in st.session_state: st.session_state.user = None
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- BARRA LATERALE FISSA ---
def crea_sidebar():
    st.sidebar.title("🏆 Menu Principale")
    st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
    st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
    st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")
    if st.session_state.user:
        st.sidebar.divider()
        st.sidebar.page_link("pages/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

crea_sidebar()

# --- CONTENUTO HOME ---
st.title("Benvenuto su FantaSchedina")
if st.session_state.user is None:
    with st.form("login"):
        em = st.text_input("Email")
        pw = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": em, "password": pw})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Errore Login")
else:
    st.success(f"Loggato come {st.session_state.user.email}")
