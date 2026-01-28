import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS per nascondere la navigazione automatica di Streamlit (i link grigi in alto)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- BARRA LATERALE PULITA ---
st.sidebar.title("Menu Principale")
st.sidebar.page_link("app.py", label="Home / Accesso Utente", icon="👤")
# Percorso corretto dopo aver rinominato la cartella in 'pagine'
st.sidebar.page_link("pagine/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pagine/3_Admin.py", label="Accesso Admin", icon="🔐")

if st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pagine/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

# --- LOGIN IN HOME ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto")
    with st.form("login"):
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.success("Accesso eseguito!")
                st.rerun()
            except:
                st.error("Credenziali errate")
else:
    st.title(f"Ciao! 👋")
    st.write(f"Utente: {st.session_state.user.email}")
    if st.button("Esci (Logout)"):
        st.session_state.user = None
        st.rerun()
