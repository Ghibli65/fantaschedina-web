import streamlit as st
from supabase import create_client, Client

# Forza il caricamento della pagina
st.set_page_config(page_title="Pannello Admin", layout="wide")

# Recupero segreti
url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

if not url or not key:
    st.error("Credenziali Supabase mancanti nei Secrets.")
    st.stop()

supabase: Client = create_client(url, key)

# --- CONTROLLO ACCESSO ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("🔒 Devi prima effettuare il login nella Home Page.")
    st.stop()

# Verifica email (deve corrispondere a quella del tuo login)
email_loggata = st.session_state.user.email
if email_loggata != "sasquit@libero.it":
    st.error(f"🚫 Accesso Negato. L'utente {email_loggata} non è l'amministratore.")
    st.stop()

# --- INTERFACCIA ADMIN ---
st.title("⚙️ Gestione Campionato")
st.write(f"Benvenuto Capo! Sei loggato come: **{email_loggata}**")

with st.form("carica_partite"):
    giornata = st.number_input("Numero Giornata", min_value=1, value=23)
    st.write("Inserisci i match della giornata:")
    
    # Creiamo 10 campi input velocemente
    nomi_partite = []
    for i in range(1, 11):
        p = st.text_input(f"Partita {i}", placeholder="Squadra A - Squadra B", key=f"match_{i}")
        nomi_partite.append(p)
    
    if st.form_submit_button("SALVA TUTTE LE PARTITE"):
        conteggio = 0
        for m in nomi_partite:
            if m.strip(): # Salva solo se il campo non è vuoto
                supabase.table("partite").insert({
                    "giornata": giornata,
                    "match": m,
                    "risultato_finale": "-"
                }).execute()
                conteggio += 1
        
        if conteggio > 0:
            st.success(f"✅ Ottimo! Hai caricato {conteggio} partite per la giornata {giornata}.")
        else:
            st.warning("Non hai inserito nessuna partita.")
