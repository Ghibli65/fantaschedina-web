import streamlit as st
from supabase import create_client, Client

# Configurazione iniziale
st.set_page_config(page_title="FantaSchedina", layout="centered")

# CSS per nascondere il menu automatico "grigio" di Streamlit
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None

# --- MENU LATERALE PERSONALIZZATO ---
st.sidebar.title("🏆 Menu Principale")

# Link alla Home (questo file)
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")

# Link ai file dentro la cartella 'pagine_app'
try:
    st.sidebar.page_link("pagine_app/2_Registrazione.py", label="Registrazione Utente", icon="📝")
    st.sidebar.page_link("pagine_app/3_Admin.py", label="Accesso Admin", icon="🔐")

    # Mostra 'Gioca' solo se l'utente è loggato
    if st.session_state.user:
        st.sidebar.divider()
        st.sidebar.page_link("pagine_app/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")
except Exception as e:
    st.sidebar.error("Errore nei link: verifica nomi cartelle su GitHub")

# --- CONTENUTO DELLA HOME ---
if st.session_state.user is None:
    st.title("Benvenuto su FantaSchedina")
    st.write("Accedi per iniziare a puntare sulla tua giornata preferita.")
    
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
    st.title(f"Bentornato!")
    st.success(f"Sei loggato come: {st.session_state.user.email}")
    if st.button("Scollegati (Logout)"):
        st.session_state.user = None
        st.rerun()
