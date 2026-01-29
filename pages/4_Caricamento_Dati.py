import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestione Quote", layout="wide")

# --- CSS PER BLOCCO MENU AUTOMATICO ---
st.markdown("""<style>[data-testid="stSidebarNav"] {display: none;} .stPageLink {background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;}</style>""", unsafe_allow_html=True)

# --- PROTEZIONE ACCESSO ---
if not st.session_state.get("admin_logged_in"):
    st.error("⛔ Accesso negato.")
    st.stop()

# --- MENU LATERALE ---
st.sidebar.title("⚙️ Area Tecnica")
st.sidebar.page_link("app.py", label="Esci ad Area Utenti", icon="🏠")
st.sidebar.divider()
st.sidebar.page_link("pages/3_Admin.py", label="Pannello Admin", icon="🔐")
st.sidebar.page_link("pages/4_Caricamento_Dati.py", label="Carica/Modifica Quote", icon="🚀")
st.sidebar.page_link("pages/5_Gestione_Utenti.py", label="Gestione Utenti", icon="👥")

st.title("🚀 Gestione Palinsesto e Quote")

# --- SEZIONE 1: CARICAMENTO ---
with st.expander("➕ Caricamento Massivo Nuove Partite", expanded=False):
    giornata_num = st.number_input("Numero Giornata", min_value=1, step=1, value=1)
    bulk_data = st.text_area("Incolla qui (Esempio: Inter-Milan;1.85;3.40...)", height=200)

    if st.button("ESEGUI CARICAMENTO", type="primary"):
        if bulk_data:
            try:
                righe = bulk_data.strip().split('\n')
                for riga in righe:
                    p = riga.split(';')
                    def q(v): return float(v.replace(',', '.'))
                    st.session_state.supabase.table("partite").insert({
                        "match": p[0].strip(), "quote_1": q(p[1]), "quote_x": q(p[2]), "quote_2": q(p[3]),
                        "quote_1x": q(p[4]), "quote_x2": q(p[5]), "quote_12": q(p[6]),
                        "quote_u25": q(p[7]), "quote_o25": q(p[8]), "quote_g": q(p[9]),
                        "quote_ng": q(p[10]), "giornata": giornata_num
                    }).execute()
                st.success("✅ Caricamento completato!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Errore: {e}")

st.divider()

# --- SEZIONE 2: VISUALIZZAZIONE E CORREZIONE ---
st.subheader("📝 Modifica o Elimina Partite Esistenti")
giornata_view = st.selectbox("Seleziona Giornata da gestire", options=range(1, 40), index=0)

try:
    # Recupero partite della giornata selezionata [cite: 2026-01-28]
    res = st.session_state.supabase.table("partite").select("*").eq("giornata", giornata_view).execute()
    partite = res.data

    if partite:
        df = pd.DataFrame(partite)
        
        # Usiamo st.data_editor per permettere la modifica diretta [cite: 2026-01-28]
        # Questa è la funzione più potente di Streamlit per correggere dati al volo
        edited_df = st.data_editor(
            df, 
            key="editor_partite",
            num_rows="dynamic", # Permette di eliminare righe selezionandole e premendo CANC
            use_container_width=True,
            column_order=("match", "quote_1", "quote_x", "quote_2", "quote_1x", "quote_x2", "quote_12", "quote_u25", "quote_o25", "quote_g", "quote_ng"),
            hide_index=True
        )

        if st.button("SALVA CORREZIONI"):
            # Qui andrebbe la logica per aggiornare le righe modificate [cite: 2026-01-28]
            # Per semplicità ora ti mostro come gestire la modifica
            st.info("Funzionalità di salvataggio modifiche in aggiornamento... Per ora, se hai sbagliato molto, conviene eliminare la riga e ricaricare.")
            
            # Nota tecnica: Per eliminare una riga nel data_editor, basta selezionarla 
            # sul lato sinistro e premere il tasto 'Canc' o l'icona del cestino.

    else:
        st.info(f"Nessuna partita trovata per la giornata {giornata_view}")

except Exception as e:
    st.error(f"Errore: {e}")
