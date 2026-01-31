import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Admin - Carica Quote", layout="wide")

# CSS per bottoni gialli e tabelle ordinate
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .stButton > button[kind="primary"] {
        background-color: #ffc107 !important;
        color: black !important;
        font-weight: bold !important;
    }
    /* Forza la visualizzazione pulita delle tabelle */
    .stDataFrame td { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

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
st.caption("Incolla la stringa. Formato: Match;1;X;2;1X;X2;12;U;O;G;NG")
input_blocco = st.text_area("Incolla qui le partite", height=150)

if st.button("ELABORA E AGGIUNGI ALLA LISTA", type="primary"):
    if input_blocco:
        righe = input_blocco.strip().split('\n')
        nuove_partite = 0
        for riga in righe:
            dati = riga.split(';')
            if len(dati) >= 11:
                try:
                    # Trasformo in float e arrotondo a 2 decimali
                    def fmt(val): return round(float(val.replace(',', '.')), 2)
                    
                    nuovo = {
                        "Match": dati[0].strip(),
                        "1": fmt(dati[1]), "X": fmt(dati[2]), "2": fmt(dati[3]),
                        "1X": fmt(dati[4]), "X2": fmt(dati[5]), "12": fmt(dati[6]),
                        "U2.5": fmt(dati[7]), "O2.5": fmt(dati[8]),
                        "G": fmt(dati[9]), "NG": fmt(dati[10]),
                        "Giornata": giornata_admin,
                        "Scadenza": f"{data_scad} {ora_scad}"
                    }
                    st.session_state.lista_partite_admin.append(nuovo)
                    nuove_partite += 1
                except:
                    st.error(f"Errore nel formato della riga: {riga[:30]}...")
        if nuove_partite > 0:
            st.success(f"✅ Aggiunte {nuove_partite} partite!")
            st.rerun()

# --- SEZIONE 3: RIEPILOGO FORMATTATO (2 DECIMALI) ---
if st.session_state.lista_partite_admin:
    st.divider()
    st.subheader(f"📋 Anteprima Giornata {giornata_admin}")
    
    df = pd.DataFrame(st.session_state.lista_partite_admin)
    
    # FORMATTAZIONE: Forza le 2 cifre decimali su tutte le colonne numeriche
    cols_quote = ["1", "X", "2", "1X", "X2", "12", "U2.5", "O2.5", "G", "NG"]
    format_dict = {col: "{:.2f}" for col in cols_quote}
    
    # Visualizzazione tabella pulita
    st.table(df[["Match"] + cols_quote].style.format(format_dict))
    
    col_del, col_save = st.columns([1, 4])
    if col_del.button("🗑️ Svuota Tutto"):
        st.session_state.lista_partite_admin = []
        st.rerun()
    
    if col_save.button("🚀 SALVA TUTTO NEL DATABASE", type="primary", use_container_width=True):
        st.balloons()
        st.success("Dati pronti per il database!")
