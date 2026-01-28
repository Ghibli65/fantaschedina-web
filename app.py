import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE E RECUPERO SEGRETI ---
# Usiamo .get() per evitare che l'app vada in crash immediato se le chiavi mancano
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

# Controllo di sicurezza: se le chiavi non sono nei Secrets, fermiamo l'app con un messaggio
if not url or not key:
    st.error("⚠️ **Errore di Configurazione:** Credenziali Supabase non trovate.")
    st.info("Vai su Streamlit Cloud -> Settings -> Secrets e inserisci SUPABASE_URL e SUPABASE_KEY.")
    st.stop()

# --- 2. CONNESSIONE AL DATABASE ---
try:
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"❌ Errore durante la connessione a Supabase: {e}")
    st.stop()

st.set_page_config(page_title="FantaSchedina - Login", layout="centered")

# Inizializzazione della sessione utente
if "user" not in st.session_state:
    st.session_state.user = None

# --- 3. LOGICA DI ACCESSO (PORTIERE) ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto a FantaSchedina")
    st.write("Accedi per giocare o crea un nuovo profilo.")
    
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
                    st.error("Email o Password errati. Riprova.")
    
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
                if not n_email or not n_pass or not n_user:
                    st.warning("Email, Password e Nome Utente sono obbligatori.")
                else:
                    try:
                        # 1. Registrazione Account in Supabase Auth
                        auth = supabase.auth.sign_up({"email": n_email, "password": n_pass})
                        if auth.user:
                            # 2. Salvataggio dati extra nella tabella 'profili'
                            supabase.table("profili").insert({
                                "id": auth.user.id, 
                                "nome": n_nome, 
                                "cognome": n_cognome,
                                "nome_utente": n_user, 
                                "cellulare": n_cell, 
                                "email": n_email
                            }).execute()
                            st.success("Iscrizione riuscita! Ora seleziona 'Accedi' sopra per entrare.")
                    except Exception as e:
                        st.error(f"Errore durante la registrazione: {e}")

else:
    # --- INTERFACCIA UTENTE LOGGATO ---
    st.title(f"Bentornato!")
    st.success(f"Sei loggato come: **{st.session_state.user.email}**")
    
    st.markdown("""
    ### 🎮 Cosa vuoi fare ora?
    Usa il menu a sinistra per:
    * **⚽ Scommettere** sulle partite della giornata.
    * **📊 Vedere i Risultati** e il tabellone generale.
    * **⚙️ Gestire il gioco** (se sei l'Admin).
    """)
    
    if st.button("Esci (Logout)"):
        st.session_state.user = None
        st.rerun()
