import streamlit as st
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Pannello Admin", layout="wide")

# --- 2. PROTEZIONE ADMIN (IL LUCCHETTO) ---
# Sostituisci 'tuaemail@esempio.it' con la tua vera email
EMAIL_ADMIN = "sasquit@libero.it" 

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 Effettua prima il login nella pagina principale.")
    st.stop()

if st.session_state.user.email != EMAIL_ADMIN:
    st.error("🚫 Accesso Negato. Non hai i permessi per gestire le partite.")
    st.stop()

# --- 3. INTERFACCIA ADMIN ---
st.title("⚙️ Pannello di Controllo Admin")
st.write(f"Benvenuto Capo! Qui puoi gestire la giornata.")

tab1, tab2 = st.tabs(["🆕 Carica Partite", "🏟️ Risultati e Quote"])

with tab1:
    st.subheader("Inserisci le 10 partite della giornata")
    with st.form("nuova_giornata"):
        giorno = st.number_input("Numero Giornata", min_value=1, value=23)
        matches = []
        for i in range(1, 11):
            m = st.text_input(f"Match {i} (es. Lazio - Genoa)", key=f"m_{i}")
            matches.append(m)
        
        if st.form_submit_button("SALVA TUTTA LA GIORNATA"):
            for m_name in matches:
                if m_name:
                    supabase.table("partite").insert({
                        "giornata": giorno,
                        "match": m_name,
                        "risultato_finale": "-"
                    }).execute()
            st.success("Partite caricate! Ora gli utenti possono scommettere.")

with tab2:
    st.info("Qui potrai inserire i risultati e le quote una volta caricate le partite.")
