import streamlit as st
from supabase import create_client, Client

# --- CONNESSIONE DATABASE ---
# Assicurati di aver inserito i Secrets su Streamlit Cloud
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="FantaSchedina - Login", layout="centered")

# Inizializzazione sessione
if "user" not in st.session_state:
    st.session_state.user = None

# --- LOGICA DI ACCESSO ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto a FantaSchedina")
    
    scelta = st.radio("Cosa vuoi fare?", ["Accedi", "Registrati"], horizontal=True)
    
    if scelta == "Accedi":
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user:
                        st.session_state.user = res.user
                        st.rerun()
                except:
                    st.error("Email o Password errati.")
    
    else:
        with st.form("reg_form"):
            st.subheader("Crea il tuo profilo")
            n_nome = st.text_input("Nome")
            n_cognome = st.text_input("Cognome")
            n_user = st.text_input("Nome Utente (es. IVANO)")
            n_email = st.text_input("Email")
            n_cell = st.text_input("Cellulare")
            n_pass = st.text_input("Password", type="password")
            
            if st.form_submit_button("ISCRIVITI ORA"):
                try:
                    # Registrazione account
                    auth = supabase.auth.sign_up({"email": n_email, "password": n_pass})
                    if auth.user:
                        # Salvataggio dati extra nella tabella profili
                        supabase.table("profili").insert({
                            "id": auth.user.id, 
                            "nome": n_nome, 
                            "cognome": n_cognome,
                            "nome_utente": n_user, 
                            "cellulare": n_cell, 
                            "email": n_email
                        }).execute()
                        st.success("Iscrizione riuscita! Ora vai su 'Accedi'.")
                except Exception as e:
                    st.error(f"Errore: {e}")

else:
    # Se loggato, mostra benvenuto
    st.title(f"Ciao {st.session_state.user.email}! 👋")
    st.info("Usa il menu a sinistra per navigare.")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
