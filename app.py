import streamlit as st
from supabase import create_client, Client
import os

st.set_page_config(page_title="FantaSchedina", layout="centered")

# Nascondiamo i link automatici in alto a sinistra
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "user" not in st.session_state: st.session_state.user = None

# --- MENU LATERALE ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")

# Definiamo i file da cercare
pagine = {
    "Registrazione": "pagine_app/2_Registrazione.py",
    "Admin": "pagine_app/3_Admin.py",
    "Gioca": "pagine_app/1_Gioca.py"
}

# Creiamo i link solo se i file esistono davvero sul server
for etichetta, percorso in pagine.items():
    if os.path.exists(percorso):
        if etichetta == "Gioca":
            if st.session_state.user:
                st.sidebar.divider()
                st.sidebar.page_link(percorso, label="VAI A GIOCARE", icon="⚽")
        else:
            st.sidebar.page_link(percorso, label=f"{etichetta} Utente", icon="📝" if "Reg" in etichetta else "🔐")
    else:
        # Se il percorso è sbagliato, Streamlit ti avviserà senza rompersi
        st.sidebar.warning(f"File non trovato: {percorso}")

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
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
