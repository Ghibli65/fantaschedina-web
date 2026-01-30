import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Test Connessione", layout="wide")

# Funzione per inizializzare Supabase [cite: 2026-01-29]
def init_connection():
    url = st.secrets.get("supabase_url")
    key = st.secrets.get("supabase_key")
    if not url or not key:
        st.error("⚠️ Mancano le chiavi nei Secrets di Streamlit!")
        return None
    return create_client(url, key)

# Prova a connetterti
if "supabase" not in st.session_state:
    st.session_state.supabase = init_connection()

if st.session_state.supabase:
    st.success("✅ Connessione a Supabase riuscita! L'URL è corretto.")
    
    st.title("⚽ FantaSchedina")
    
    # Form di Login semplice
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("ENTRA", type="primary"):
        try:
            # Tentativo di login [cite: 2026-01-29]
            res = st.session_state.supabase.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            st.session_state.user = res.user
            st.rerun()
        except Exception as e:
            st.error(f"Credenziali non valide o errore: {e}")

if "user" in st.session_state:
    st.write(f"Benvenuto, {st.session_state.user.email}!")
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()
