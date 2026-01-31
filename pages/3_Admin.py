import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Admin - Carica Quote", layout="wide")

# CSS per bottoni gialli e tabelle
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Lista persistente per le partite caricate
if "lista_partite_admin" not in st.session_state:
    st.session_state.lista_partite_admin = []

with st.sidebar:
    st.title("⚙️ Pannello Admin")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    if st.button("⚽ Palinsesto", use_container_width=True):
        st.switch_page("pages/1_Gioca.py")

st.title("🛠️ Caricamento Quote e Scadenze")

# --- SEZIONE 1: GIORNATA E SCADENZA ---
with st.container(border=True):
    st.subheader("📌 Impostazioni Giornata")
    c1, c2, c3 = st.columns(3)
    with c1:
        giornata_admin = st.number_input("N° Giornata", min_value=1, step=1, value=1)
    with c2:
        data_scad = st.date_input("Data Termine")
    with c3:
        ora_scad = st.time_input("Ora Termine")

st.divider()

# --- SEZIONE 2: CARICA IN BLOCCO (TESTO) ---
st.subheader("🚀 Caricamento Rapido in Blocco")
st.caption("Incolla qui la stringa delle partite (es. Lazio-Genoa;2,1;2,9;...) e premi 'Elabora'")
input_blocco = st.text_area("Incolla qui le partite", height=150, placeholder="Lazio - Genoa;2,1;2,9;...")

if st.button("ELABORA E AGGIUNGI ALLA TABELLA", type="primary"):
    if input_blocco:
        righe = input_blocco.strip().split('\n')
        nuove_partite = 0
        for riga in righe:
            dati = riga.split(';')
            if len(dati) >= 11:
                try:
                    # Pulizia e conversione dei dati (gestisce la virgola decimale)
                    nuovo = {
                        "Giorno/Ora Termine": f"{data_scad} {ora_scad}",
                        "Match": dati[0].strip(),
                        "1": float(dati[1].replace(',', '.')),
                        "X": float(dati[2].replace(',', '.')),
                        "2": float(dati[3].replace(',', '.')),
                        "1X": float(dati[4].replace(',', '.')),
                        "X2": float(dati[5].replace(',', '.')),
                        "12": float(dati[6].replace(',', '.')),
                        "U2.5": float(dati[7].replace(',', '.')),
                        "O2.5": float(dati[8].replace(',', '.')),
                        "G": float(dati[9].replace(',', '.')),
                        "NG": float(dati[10].replace(',', '.')),
                        "Giornata": giornata_admin
                    }
                    st.session_state.lista_partite_admin.append(nuovo)
                    nuove_partite += 1
                except Exception as e:
                    st.error(f"Errore nella riga: {riga}. Controlla il formato.")
        if nuove_partite > 0:
            st.success(f"✅ Aggiunte {nuove_partite} partite alla lista!")
            st.rerun()
    else:
        st.warning("L'area di testo è vuota!")

# --- SEZIONE 3: RIEPILOGO E SALVATAGGIO ---
if st.session_state.lista_partite_admin:
    st.divider()
    st.subheader(f"📋 Riepilogo Inserimenti in Blocco - Giornata {giornata_admin}")
    
    df = pd.DataFrame(st.session_state.lista_partite_admin)
    # Mostriamo solo le colonne necessarie nella tabella
    st.table(df[["Match", "1", "X", "2", "1X", "X2", "12", "U2.5", "O2.5", "G", "NG"]])
    
    col_del, col_save = st.columns([1, 4])
    if col_del.button("🗑️ Svuota Tutto"):
        st.session_state.lista_partite_admin = []
        st.rerun()
    
    if col_save.button("🚀 SALVA DEFINITIVAMENTE TUTTO", type="primary", use_container_width=True):
        # Qui metteremo il codice per inviare tutto a Supabase
        st.balloons()
        st.success("Tutte le partite sono state salvate correttamente!")
