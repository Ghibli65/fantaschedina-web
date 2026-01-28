import streamlit as st
from supabase import create_client, Client

# --- RECUPERO SEGRETI ---
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if not url or "tuoidprogetto" in url:
    st.error("⚠️ URL di Supabase non valido nei Secrets! Inserisci il tuo link reale.")
    st.stop()

# --- CONNESSIONE ---
try:
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Errore di connessione: {e}")
    st.stop()

st.set_page_config(page_title="FantaSchedina - Login", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

# --- PORTIERE (LOGIN/REGISTRAZIONE) ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto a FantaSchedina")
    scelta = st.radio("Cosa vuoi fare?", ["Accedi", "Registrati"], horizontal=True)
    
    if scelta == "Accedi":
        with st.form("login_form"):
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                    if res.user:
                        st.session_state.user = res.user
                        st.rerun()
                except:
                    st.error("Credenziali errate.")
    
    else:
        with st.form("reg_form"):
            st.subheader("Crea il tuo profilo")
            col1, col2 = st.columns(2)
            with col1:
                n_nome = st.text_input("Nome")
                n_user = st.text_input("Nome Utente (es. IVANO)")
                n_email = st.text_input("Email")
            with col2:
                n_cognome = st.text_input("Cognome")
                n_cell = st.text_input("Cellulare")
                n_pass = st.text_input("Password", type="password")
            
            if st.form_submit_button("ISCRIVITI ORA"):
                try:
                    auth = supabase.auth.sign_up({"email": n_email, "password": n_pass})
                    if auth.user:
                        supabase.table("profili").insert({
                            "id": auth.user.id, "nome": n_nome, "cognome": n_cognome,
                            "nome_utente": n_user, "cellulare": n_cell, "email": n_email
                        }).execute()
                        st.success("Iscrizione riuscita! Ora fai il login.")
                except Exception as e:
                    st.error(f"Errore: {e}")
else:
    st.title(f"Ciao {st.session_state.user.email}! 👋")
    st.info("Usa il menu a sinistra per navigare.")
    if st.button("Esci (Logout)"):
        st.session_state.user = None
        st.rerun()
