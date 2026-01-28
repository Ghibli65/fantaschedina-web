import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Gestione Campionato", layout="wide")

# Connessione
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("⚙️ Pannello Amministratore")

# --- SEZIONE CARICAMENTO PARTITE ---
st.header("1. Carica Partite della Giornata")
with st.form("form_partite"):
    giornata = st.number_input("Numero Giornata", min_value=1, value=23, step=1)
    st.write("Inserisci i 10 match (es: Inter - Milan):")
    
    partite_input = []
    col1, col2 = st.columns(2)
    for i in range(1, 11):
        with col1 if i <= 5 else col2:
            m = st.text_input(f"Match {i}", key=f"m{i}")
            partite_input.append(m)
    
    if st.form_submit_button("SALVA GIORNATA"):
        caricate = 0
        for match in partite_input:
            if match.strip():
                supabase.table("partite").insert({
                    "giornata": giornata,
                    "match": match,
                    "risultato_finale": "-"
                }).execute()
                caricate += 1
        st.success(f"✅ Hai caricato {caricate} partite per la giornata {giornata}!")

st.divider()

# --- SEZIONE AGGIORNAMENTO RISULTATI ---
st.header("2. Inserisci Risultati Finali")
st.write("Usa questa sezione a fine giornata per calcolare i punteggi.")
# (Qui aggiungeremo il calcolo punti appena carichi le prime partite)
