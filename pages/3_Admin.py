import streamlit as st
from supabase import create_client, Client

# Connessione (Streamlit riusa i secrets che hai già messo)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Pannello Admin", layout="wide")

# PROTEZIONE: Solo tu (sasquit@libero.it) vedi questa pagina
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Fai il login in Home Page")
    st.stop()

if st.session_state.user.email != "sasquit@libero.it":
    st.error("Accesso negato")
    st.stop()

st.title("⚙️ Gestione Campionato")

# FORM PER CARICARE LE PARTITE
with st.form("carica_partite"):
    giornata = st.number_input("Numero Giornata", min_value=1, value=23)
    st.write("Inserisci i match:")
    m1 = st.text_input("Partita 1")
    m2 = st.text_input("Partita 2")
    m3 = st.text_input("Partita 3")
    # ... ne mettiamo 3 per ora per testare veloce ...
    
    if st.form_submit_button("SALVA PARTITE"):
        partite = [m1, m2, m3]
        for m in partite:
            if m:
                supabase.table("partite").insert({
                    "giornata": giornata,
                    "match": m,
                    "risultato_finale": "-"
                }).execute()
        st.success(f"Giornata {giornata} caricata con successo!")
