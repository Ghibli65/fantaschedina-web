import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# Nasconde i link automatici di Streamlit in alto
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "user" not in st.session_state: st.session_state.user = None

# --- MENU LATERALE ---
st.sidebar.title("Menu Principale")
st.sidebar.page_link("app.py", label="Home / Accesso Utente", icon="👤")
st.sidebar.page_link("pagine_app/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pagine_app/3_Admin.py", label="Accesso Admin", icon="🔐")

if st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pagine_app/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

# --- LOGIN ---
if st.session_state.user is None:
    st.title("🏆 FantaSchedina")
    with st.form("login"):
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Errore Login")
else:
    st.title("Bentornato! 👋")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
