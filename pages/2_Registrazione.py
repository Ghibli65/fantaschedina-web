import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Registrazione", layout="centered")

# --- CSS PER BLOCCARE IL MENU (Lo stesso di app.py) ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}
    .stButton>button {width: 100%; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Supabase (usando i secrets dell'app)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- BARRA LATERALE FISSA ---
st.sidebar.title("🏆 Menu Principale")
st.sidebar.page_link("app.py", label="Home / Login", icon="👤")
st.sidebar.page_link("pages/2_Registrazione.py", label="Registrazione Utente", icon="📝")
st.sidebar.page_link("pages/3_Admin.py", label="Accesso Admin", icon="🔐")

if "user" in st.session_state and st.session_state.user:
    st.sidebar.divider()
    st.sidebar.page_link("pages/1_Gioca.py", label="VAI A GIOCARE", icon="⚽")

# --- FORM DI REGISTRAZIONE ---
st.title("📝 Registrazione")
st.write("Inserisci i tuoi dati per creare un profilo e iniziare a giocare.")

with st.form("form_registrazione"):
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome")
    cognome = col2.text_input("Cognome")
    
    cellulare = st.text_input("Numero di Cellulare (Verrà usato come Nome Utente)")
    email = st.text_input("Email")
    password = st.text_input("Password (minimo 6 caratteri)", type="password")
    
    submit = st.form_submit_button("REGISTRAMI ORA")

    if submit:
        if nome and cognome and cellulare and email and len(password) >= 6:
            try:
                # Registrazione su Supabase Auth con dati extra nei metadati [cite: 2026-01-28]
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "nome": nome,
                            "cognome": cognome,
                            "cellulare": cellulare
                        }
                    }
                })
                st.success("✅ Registrazione riuscita! Ora puoi tornare nella Home per fare il Login.")
                st.balloons()
            except Exception as e:
                st.error(f"Errore durante la registrazione: {e}")
        else:
            st.warning("⚠️ Per favore, compila tutti i campi. La password deve avere almeno 6 caratteri.")
