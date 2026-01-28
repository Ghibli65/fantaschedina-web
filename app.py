import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE PAGINA (Deve essere la prima istruzione) ---
st.set_page_config(page_title="FantaSchedina", layout="centered")

# --- 2. CONNESSIONE SUPABASE ---
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if not url or "tuoidprogetto" in url:
    st.error("❌ Configurazione mancante nei Secrets di Streamlit!")
    st.stop()

try:
    # Inizializziamo il client Supabase una sola volta
    if "supabase" not in st.session_state:
        st.session_state.supabase = create_client(url, key)
    supabase = st.session_state.supabase
except Exception as e:
    st.error(f"Errore di connessione: {e}")
    st.stop()

# --- 3. GESTIONE SESSIONE UTENTE ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- 4. INTERFACCIA ---
if st.session_state.user is None:
    st.title("🏆 Benvenuto a FantaSchedina")
    st.write("Accedi per giocare o gestire il campionato.")
    
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
                        st.success("Accesso eseguito!")
                        st.rerun()
                except Exception as ex:
                    st.error("Credenziali non valide o errore di rete.")
    
    else:
        with st.form("register_form"):
            st.subheader("Nuovo Profilo")
            n_email = st.text_input("Email")
            n_pass = st.text_input("Password (min. 6 caratteri)", type="password")
            n_user = st.text_input("Nome Utente (es: Ghibli65)")
            
            if st.form_submit_button("ISCRIVITI"):
                try:
                    auth = supabase.auth.sign_up({"email": n_email, "password": n_pass})
                    if auth.user:
                        # Creiamo anche il record nella tabella profili
                        supabase.table("profili").insert({
                            "id": auth.user.id, 
                            "email": n_email,
                            "nome_utente": n_user
                        }).execute()
                        st.success("Registrazione completata! Ora puoi fare il login.")
                except Exception as ex:
                    st.error(f"Errore: {ex}")

else:
    # COSA VEDE L'UTENTE LOGGATO
    st.title(f"Ciao {st.session_state.user.email}! 👋")
    st.info("👈 Apri il menu a sinistra per navigare tra le pagine.")
    
    # Questo tasto serve solo se la barra laterale è pigra a caricarsi
    if st.sidebar.button("Aggiorna Menu"):
        st.rerun()

    if st.button("Esci (Logout)"):
        st.session_state.user = None
        st.rerun()
