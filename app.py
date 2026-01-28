import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="FantaSchedina", layout="centered")

# Inizializzazione Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

if "user" not in st.session_state:
    st.session_state.user = None

# --- BARRA LATERALE PERSONALIZZATA ---
st.sidebar.title("Menu Principale")

# 1. Accesso Utente (Home)
st.sidebar.page_link("app.py", label="Home / Accesso Utente", icon="👤")

# 2. Registrazione (Creeremo questo file tra un attimo)
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")

# 3. Accesso Admin
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

# Se l'utente è loggato, mostriamo anche il tasto per Giocare
if st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pages/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

# --- CONTENUTO HOME PAGE (LOGIN) ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto su FantaSchedina")
    with st.form("login_form"):
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("ACCEDI"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.success("Login effettuato!")
                st.rerun()
            except:
                st.error("Credenziali errate")
else:
    st.title(f"Ciao {st.session_state.user.email}! 👋")
    st.info("Usa il menu a sinistra per navigare.")
    if st.button("Esci (Logout)"):
        st.session_state.user = None
        st.rerun()
