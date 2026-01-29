import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Utenti", layout="wide")

# --- CSS PER BLOCCO MENU AUTOMATICO ---
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# --- PROTEZIONE ACCESSO ---
if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato. Effettua il login come Admin.")
    st.stop()

# --- MENU LATERALE ADMIN (Coerente su tutte le pagine admin) ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

# --- CONTENUTO ---
st.title("👥 Elenco Giocatori Iscritti")
st.info("Qui puoi vedere tutti gli utenti che hanno completato la registrazione.")

try:
    # Recuperiamo i dati dalla tabella profiles [cite: 2026-01-28]
    response = st.session_state.supabase.table("profiles").select("*").execute()
    data = response.data

    if data:
        # Creiamo la tabella con Pandas [cite: 2026-01-28]
        df = pd.DataFrame(data)
        
        # Pulizia colonne per la visualizzazione [cite: 2026-01-28]
        df = df.rename(columns={
            "username": "Nickname",
            "nome": "Nome",
            "cognome": "Cognome",
            "email": "Email",
            "cellulare": "Cellulare",
            "created_at": "Data Iscrizione"
        })
        
        # Mostra tabella [cite: 2026-01-28]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success(f"Totale utenti registrati: {len(df)}")
    else:
        st.warning("Nessun utente trovato nel database.")

except Exception as e:
    st.error(f"Errore tecnico: {e}")
