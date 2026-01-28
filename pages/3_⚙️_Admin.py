import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE ---
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if not url or not key:
    st.error("Credenziali non trovate.")
    st.stop()

supabase: Client = create_client(url, key)

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- 2. PROTEZIONE ADMIN ---
# Qui ho messo l'email che vedo dal tuo screenshot
EMAIL_ADMIN = "sasquit@libero.it" 

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 Effettua prima il login nella pagina principale.")
    st.stop()

if st.session_state.user.email != EMAIL_ADMIN:
    st.error(f"🚫 Accesso Negato per {st.session_state.user.email}. Solo l'Admin può entrare.")
    st.stop()

# --- 3. INTERFACCIA ---
st.title("⚙️ Pannello Admin")
st.success(f"Benvenuto Capo ({st.session_state.user.email})")

tab1, tab2 = st.tabs(["🆕 Carica Partite", "🏟️ Gestione Risultati"])

with tab1:
    with st.form("carica_match"):
        giornata = st.number_input("Giornata n.", min_value=1, value=23)
        st.write("Inserisci i match (es. Lazio-Genoa)")
        matches = [st.text_input(f"Partita {i}", key=f"m{i}") for i in range(1, 11)]
        
        if st.form_submit_button("CARICA GIORNATA"):
            for m in matches:
                if m:
                    supabase.table("partite").insert({
                        "giornata": giornata, "match": m, "risultato_finale": "-"
                    }).execute()
            st.success("Giornata caricata!")

with tab2:
    st.write("Qui appariranno i match caricati per inserire i risultati.")
